
from sensors.SensorBase import I2CSensorBase, SensorEvent
import time
import logging

# Commands
_CMD       = 0x80
_CMD_CLEAR = 0x40
_CMD_WORD  = 0x20
_CMD_BLOCK = 0x10

# Registers
_REG_CONTROL   = 0x00
_REG_TIMING    = 0x01
_REG_ID        = 0x0A
_REG_BLOCKREAD = 0x0B
_REG_DATA0     = 0x0C
_REG_DATA1     = 0x0E


# Control parameters
TSL2561_POWER_ON = 0x03
TSL2561_POWER_OFF = 0x00

# Timing parameters
_GAIN_1          = 0b00000000
_GAIN_16         = 0b00010000
_INTEGRATION_START = 0b00001000
_INTEGRATION_STOP  = 0b00000000
_INTEGRATE_13      = 0b00000000
_INTEGRATE_101     = 0b00000001
_INTEGRATE_402     = 0b00000010
_INTEGRATE_DEFAULT = _INTEGRATE_402
_INTEGRATE_NA      = 0b00000011

# Possible I2C addresses of the sensor
TSL2561_I2CADDR_GND = 0x29
TSL2561_I2CADDR_FLOAT = 0x39
TSL2561_I2CADDR_VCC = 0x49

class TSL2561(I2CSensorBase):
    '''Access TSL2561 based light-to-digital convertor.
    
    Example:
    
    import smbus
    import tsl2561
    
    bus = smbus.SMBus(1)
    sensor = tsl2561.Tsl2561(bus)
    print sensor.lux
    '''
    
    GainTbl = [
        {
            'integ': _INTEGRATE_13, 
            'delay': 0.15,
            'gain': _GAIN_1, 
            'threshold': 8842,
            'factor': 16.0 / 0.034, # 470.6
        },
        {
            'integ': _INTEGRATE_101,
            'delay': 0.103, 
            'gain': _GAIN_1, 
            'threshold': 30358,
            'factor': 16.0 / 0.252, # 63.5
        },
        {
            'integ': _INTEGRATE_13,
            'delay': 0.15, 
            'gain': _GAIN_16, 
            'threshold': 35651,
            'factor': 1.0 / 0.034, # 29.4
        },
        {
            'integ': _INTEGRATE_402,
            'delay': 0.405, 
            'gain': _GAIN_1, 
            'threshold': 16254,
            'factor': 16.0 / 1.0, # 16.0
        },
        {
            'integ': _INTEGRATE_101,
            'delay': 0.103, 
            'gain': _GAIN_16, 
            'threshold': 16514,
            'factor': 1.0 / 0.252, # 3.96
        }, 
        {
            'integ': _INTEGRATE_402,
            'delay': 0.405, 
            'gain': _GAIN_16, 
            'threshold': 0,
            'factor': 1.0,
        }, 
    ]
    
    def __init__(self, sensor_name, bus=None, addr=TSL2561_I2CADDR_GND):
        '''Initializes the sensor with some default values.

        bus: The SMBus descriptor on which this sensor is attached.
        addr: The I2C bus address
            (default is 0x39).
        '''

        I2CSensorBase.__init__(
            self, 
            sensor_name=sensor_name,
            bus=bus,
            address=addr)

        # TODO: Only power on when necessary
        self._setPowerState(TSL2561_POWER_ON)


    def _readRawData(self):
        '''Read the raw sensor data for both (infrared and normal light) 
        channels.'''
        
        gi = len(TSL2561.GainTbl) - 1
        self._setTiming(gi)
        
        while True:
            cmd = _CMD | _CMD_WORD | _REG_DATA0
            vals = self._bus.read_i2c_block_data(self._address, cmd, 2)
            channel0 = vals[1] << 8 | vals[0]
    
            cmd = _CMD | _CMD_WORD | _REG_DATA1
            vals = self._bus.read_i2c_block_data(self._address, cmd, 2)
            channel1 = vals[1] << 8 | vals[0]

            self._logger.debug('gi {0}, ch0 {1}, ch2 {2}'.format(gi, channel0, channel1)) 

            if (channel0 == 0xffff) or (channel1 == 0xffff):
                if gi > 0:
                    gi = gi - 1
                    self._setTiming(gi)
                else:
                    return (gi, channel0, channel1)
            else:
                return (gi, channel0, channel1)


    def _calcLuminosity(self, gi, channel0, channel1):
        '''Calculate the luminosity from raw channel values.
        
        Code is taken from https://github.com/sparkfun/
         TSL2561_Luminosity_Sensor_BOB/blob/master/
         Libraries/SFE_TSL2561/SFE_TSL2561.cpp
        
        :param int channel0: The raw channel value for channel 0.
        :param int channel1: The raw channel value for channel 0.
        
        :returns: The luminosity in Lux. 
        '''
        
        # Check for sensor saturation / channel overflow
        if (gi == 0) and (channel0 == 0xffff or channel1 == 0xffff):
            return None
        
        # Check if channel0 is completely dark (prevent div by 0)
        if (channel0 == 0):
            return 0.0
        
        d0 = float(channel0)
        d1 = float(channel1)
        
        ratio = d1 / d0

        d0 = d0 * TSL2561.GainTbl[gi]['factor']
        d1 = d1 * TSL2561.GainTbl[gi]['factor']

        #if (self._gain == _GAIN_16):
        #    d0 = d0 / 16
        #    d1 = d1 / 16

        if (ratio < 0.5):
            lum = 0.0304 * d0 - 0.062 * d0 * (ratio ** 1.4)
        elif (ratio < 0.61):
            lum = 0.0224 * d0 - 0.031 * d1
        elif (ratio < 0.80):
            lum = 0.0128 * d0 - 0.0153 * d1
        elif (ratio < 1.30):
            lum = 0.00146 * d0 - 0.00112 * d1
        else:
            lum = 0.0
            
        return lum
        

    def sampleValues(self, valuetype=None):
        '''Sample sensor values and return results as sensor events.
        
        :returns: List of sensor event objects.
        '''
        
        # TODO: Implement auto-range
        (gi, ch0, ch1) = self._readRawData()
        
        lum = self._calcLuminosity(gi, ch0, ch1)

        return [
            SensorEvent(self, lum, 'Lx', 'luminosity', '{s} {q} = {v} {u}')
        ]

    def _setPowerState(self, pwr_state):
        '''Set the sensor power state.
        
        :param int pwr_state: Either TSL2561_PWR_ON or TSL2561_PWR_OFF.'''
        
        cmd = _CMD | _REG_CONTROL
        self._bus.write_byte_data(self._address, cmd, pwr_state)

        # Wait for 400ms to be power up.
        time.sleep(0.4)

    def _setTiming(self, gain_index):
        '''Write to the timing register.'''
        
        gain = TSL2561.GainTbl[gain_index]['gain']
        integ = TSL2561.GainTbl[gain_index]['integ']
        delay = TSL2561.GainTbl[gain_index]['delay']
        
        cmd = _CMD | _REG_TIMING
        self._bus.write_byte_data(self._address, cmd, gain | integ)

        # Wait for 400ms to complete initial A/D conversion.
        time.sleep(delay + 0.100)
