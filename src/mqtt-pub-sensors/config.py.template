# $Id: config.py 61 2015-04-05 00:44:07Z andreas $

import logging
from sensors.RPiInternalTemp import RPiInternalTemp

def get_sensors():
    '''Set up the sensors.'''

    #bus = smbus.SMBus(1)

    sensors = [
        #'bmp180': BMP180('BMP180', bus), 
        #'htu21d': HTU21D('HTU21D', 1), # different interface, needs bus number, not smbus object
        #'tsl2561': TSL2561('TSL2561', bus),
        RPiInternalTemp('cputemp')
    ]

    return sensors


config = {
    # node name as used in the mqtt topic path
    'node_name': 'dirac',
    
    # Hostname of the MQTT broker
    'mqtt_broker': 'bpi1',

    # The topic name is constructed from sensor name and measured quantity 
    # (temperature, pressure, ...). The prefix is prepended to the topic path.
    'mqtt_topic_prefix': '/sensors',

    # Log file 
    'log_file': 'mqtt-pub-sensors.log',

    # Log level
    'log_level': logging.INFO,
}

