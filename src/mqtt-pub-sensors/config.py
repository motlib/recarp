'''Configuration file for mqtt-pub-sensor.'''

import logging

config = {
    # Hostname of the MQTT broker
    'mqtt_broker': 'rpi1',

    # The topic name is constructed from sensor name and measured quantity 
    # (temperature, pressure, ...). The prefix is prepended to the topic path.
    'mqtt_topic_prefix': '/sensors',

    # Sample time interval in seconds.
    'sample_interval': 60,

    # Log file 
    'log_file': 'mqtt-pub-sensors.log',

    # Log level
    'log_level': logging.INFO,
}

