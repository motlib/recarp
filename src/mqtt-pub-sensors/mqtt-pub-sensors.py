# $Id: mqtt-pub-sensors.py 61 2015-04-05 00:44:07Z andreas $

import paho.mqtt.publish as mqtt
from sensors.BMP180 import BMP180
from sensors.HTU21D import HTU21D
from sensors.TSL2561 import TSL2561
from sensors.RPiInternalTemp import RPiInternalTemp
import logging
import smbus
import time
from config import config


def init():
    '''Initialize runtime system.'''

    # set up logging level and format
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s', 
        level=config['log_level'],
        filename=config['log_file'])


def setup_sensors():
    '''Set up the sensors.'''

    logging.info('Setting up sensors')

    bus = smbus.SMBus(1)

    sensors = [
        BMP180('BMP180', bus), 
        HTU21D('HTU21D', 1), # other interface, needs bus number, not smbus object
        TSL2561('TSL2561', bus),
        RPiInternalTemp('RPi3')
    ]

    return sensors


def main():    
    '''Application main entry point.

    Set up the sensors and publish cyclic updates of the sensor values
    to the MQTT broker.
    '''

    init()
    
    sensors = setup_sensors()
    
    logging.info('Start sending events to MQTT broker.')
    
    while True:
        sens_evts = []
        
        for s in sensors:
            sens_evts.extend(s.sampleValues())

        for evt in sens_evts:
            mqtt_path = '{p}/{n}/{q}'.format(
                p=config['mqtt_topic_prefix'],
                n=evt.getSensor().getName(),
                q=evt.getQuantity()) 

            mqtt_val = str(evt.getValue())

            # The publish might fail, e.g. due to network problems. Just log 
            # the exception and try again next time.
            try:
                mqtt.single(
                    mqtt_path, 
                    mqtt_val, 
                    hostname=config['mqtt_broker'])
            except:
                logging.exception('Publish of single MQTT value failed.')
                   
        time.sleep(config['sample_interval'])


if __name__ == '__main__':
    main()
