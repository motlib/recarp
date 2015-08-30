# $Id: mqtt-pub-sensors.py 61 2015-04-05 00:44:07Z andreas $


import logging
import time
import json
import os

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from config import config, get_sensors

def init_runtime():
    '''Initialize runtime system.'''

    # set up logging level and format
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s', 
        level=logging.DEBUG)
        #filename=config['logfile#'])

        
def mqtt_connect():
    host = config['mqtt_broker'];
    msg = "Connecting to mqtt broker '{0}'."
    logging.info(msg.format(host))

    mqtt_clt = mqtt.Client()
    #mqtt_clt.connect(host=host)
    #mqtt_clt.loop_start()
    logging.info('Connection established.')

    return mqtt_clt
    

def get_mqtt_path(evt):

    data = {
        'prefix': config['mqtt_topic_prefix'],
        'node': config['node_name'],
        'sensor': evt.getSensor().getName(),
        'quantity': evt.getQuantity(),
    }

    path_tmpl = '{prefix}/{node}/{sensor}/{quantity}'
    
    return path_tmpl.format(**data)


def get_mqtt_message(evt):
    
    value = {
        'time': evt.getTimestamp().isoformat(),
        'sensor_name': evt.getSensor().getName(),
        'quantity': evt.getQuantity(),
        'unit': evt.getUnit(),
        'value': evt.getValue(),
    }
    
    return json.dumps(value, sort_keys=True, indent=4)

    
def main():    
    '''Application main entry point.

    Set up the sensors and publish cyclic updates of the sensor values to the 
    MQTT broker.'''

    init_runtime()
    
    logging.info('Setting up sensors')
    sensors = get_sensors()

    mqtt_clt = mqtt_connect()
    
    while True:
        sens_evts = []

        for s in sensors:
            logging.debug('Reading sensor ' + s.getName())
            sens_evts.extend(
                s.sampleValues())
            logging.debug('Got result.')

        logging.debug('Publishing data.')
        for evt in sens_evts:
            mqtt_path = get_mqtt_path(evt)
            mqtt_msg = get_mqtt_message(evt)

            # The publish might fail, e.g. due to network problems. Just log 
            # the exception and try again next time.
            try:
                publish.single(
                    topic=mqtt_path,
                    payload=mqtt_msg,
                    hostname=config['mqtt_broker'])
#                mqtt_clt.publish(
#                    mqtt_path, 
#                    mqtt_msg)
            except:
                logging.exception('Publish of MQTT value failed.')
                   
        #time.sleep(config['sample_interval'])
        time.sleep(5)


if __name__ == '__main__':
    main()
