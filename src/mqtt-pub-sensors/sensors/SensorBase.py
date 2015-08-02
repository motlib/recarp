'''
Created on Mar 8, 2015

@author: andreas
'''

import logging
from datetime import datetime

class SensorError(Exception):
    '''Base class for all kind of errors related to accessing a sensor.'''
    pass


class ChecksumError(SensorError):
    '''Checksum mismatch error.'''
    pass


class SensorEvent():
    def __init__(self, sensor, value, unit, quantity, fmt='{s} {q} = {v} {u}'):
        self._sensor = sensor
        self._value = value
        self._unit = unit
        self._quantity = quantity
        self._strfmt = fmt

        self._timestamp = datetime.utcnow()
    
    
    def getValue(self):
        return self._value
 
    
    def getUnit(self):
        return self._unit
    
    
    def getQuantity(self):
        return self._quantity
    
    
    def getTimestamp(self):
        return self._timestamp


    def getSensor(self):
        return self._sensor
    
    def __str__(self):
        return self._strfmt.format(
            s=self._sensor,
            q=self._quantity, 
            v=self._value, 
            u=self._unit)


class SensorBase(object):
    def __init__(self, sensor_name):
        
        self._sensor_name = sensor_name
        self._description = ''
        
        # set up a logger
        self._logger = logging.getLogger(
            "Sensor_'{0}'".format(
                sensor_name))
                
    def getName(self):
        return self._sensor_name
    
    def getDescription(self):
        return self._description
    
    def setDescription(self):
        self._description = ''
        
    def __str__(self):
        return "Sensor_{0}".format(
            self._sensor_name)
        
    def sampleValues(self):
        pass
        

        
class I2CSensorBase(SensorBase):
    def __init__(self, sensor_name, bus, address):
        
        SensorBase.__init__(self, sensor_name)
        
        assert(bus is not None)
        
        self._address = address
        self._bus = bus
