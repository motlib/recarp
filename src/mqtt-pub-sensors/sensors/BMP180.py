#!/usr/bin/env python


from sensors.SensorBase import I2CSensorBase, SensorEvent
import struct
import time

# Default I2C address
_DEFAULT_ADDRESS = 0x77

# Registers
_REG_AC1                 = 0xAA
_REG_AC2                 = 0xAC
_REG_AC3                 = 0xAE
_REG_AC4                 = 0xB0
_REG_AC5                 = 0xB2
_REG_AC6                 = 0xB4
_REG_B1                  = 0xB6
_REG_B2                  = 0xB8
_REG_MB                  = 0xBA
_REG_MC                  = 0xBC
_REG_MD                  = 0xBE
_REG_CALIB_OFFSET        = _REG_AC1
_REG_CONTROL_MEASUREMENT = 0xF4
_REG_DATA                = 0xF6

# Commands
_CMD_START_CONVERSION    = 0b00100000
_CMD_TEMPERATURE         = 0b00001110
_CMD_PRESSURE            = 0b00010100

# Oversampling mode
OS_MODE_SINGLE = 0b00
OS_MODE_2      = 0b01
OS_MODE_4      = 0b10
OS_MODE_8      = 0b11

# Conversion time (in second)
_WAIT_TEMPERATURE = 0.0045
_WAIT_PRESSURE    = [0.0045, 0.0075, 0.0135, 0.0255]

class BMP180(I2CSensorBase):
    def __init__(self, sensor_name, bus=None):
        

        I2CSensorBase.__init__(
            self, 
            sensor_name=sensor_name, 
            bus=bus, 
            address=0x77)

        self._ds_defaults = False

        self._ac0 = None
        self._ac1 = None
        self._ac2 = None
        self._ac3 = None
        self._ac4 = None
        self._ac5 = None
        self._ac6 = None
        self._b1 = None
        self._b2 = None
        self._mb = None
        self._mc = None
        self._md = None
        self._os_mode = OS_MODE_SINGLE

        self._readCalData()
        


    @property
    def os_mode(self):
        '''Gets/Sets oversampling mode.

        OS_MODE_SINGLE: Single mode.
        OS_MODE_2: 2 times.
        OS_MODE_4: 4 times.
        OS_MODE_8: 8 times.

        '''
        return (self._os_mode)

    @os_mode.setter
    def os_mode(self, os_mode):
        assert(os_mode == OS_MODE_SINGLE
               or os_mode == OS_MODE_2
               or os_mode == OS_MODE_4
               or os_mode == OS_MODE_8)
        self._os_mode = os_mode

    def _readCalData(self):
        calib = self._bus.read_i2c_block_data(
            self._address,
            _REG_CALIB_OFFSET, 
            22)
        (self._ac1, self._ac2, self._ac3, self._ac4,
         self._ac5, self._ac6, self._b1, self._b2,
         self._mb, self._mc, self._md) = struct.unpack(
             '>hhhHHHhhhhh', ''.join([chr(x) for x in calib]))


    def _readRawTemp(self):
        
        if self._ds_defaults == True:
            return 27898
        
        cmd = _CMD_START_CONVERSION | _CMD_TEMPERATURE
        self._bus.write_byte_data(self._address,
            _REG_CONTROL_MEASUREMENT, cmd)
        
        time.sleep(_WAIT_TEMPERATURE)

        vals = self._bus.read_i2c_block_data(self._address,
             _REG_DATA, 2)
        
        t_raw = vals[0] << 8 | vals[1]

        return t_raw
        
        
    def _readRawPressure(self):
        
        if self._ds_defaults == True:
            return 23843
        
        self._bus.write_byte_data(
            self._address,
            _REG_CONTROL_MEASUREMENT, 
            _CMD_START_CONVERSION | self._os_mode << 6 | _CMD_PRESSURE)
        
        time.sleep(_WAIT_PRESSURE[self._os_mode])
        
        vals = self._bus.read_i2c_block_data(
            self._address,
            _REG_DATA, 
            3)
        p_raw = (vals[0] << 16 | vals[1] << 8 | vals[0]) >> (8 - self._os_mode)

        return p_raw
        
        
    def _calcTemperature(self, t_raw):
        x1 = ((t_raw - self._ac6) * self._ac5) >> 15
        x2 = (self._mc << 11) / (x1 + self._md)
        b5 = x1 + x2
        _temperature = ((b5 + 8) / 2**4) / 10.0

        return _temperature
        
        
    def _calcPressure(self, t_raw, p_raw):
        
        x1 = ((t_raw - self._ac6) * self._ac5) >> 15
        x2 = (self._mc << 11) / (x1 + self._md)
        b5 = x1 + x2

        b6 = b5 - 4000
        x1 = self._b2 * ((b6 * b6) >> 12)
        x2 = self._ac2 * b6
        x3 = (x1 + x2) >> 11
        b3 = (((self._ac1 *4 + x3) << self._os_mode) + 2) >> 2
        x1 = (self._ac3 * b6) >> 13
        x2 = (self._b1 * (b6 * b6) >> 12) >> 16
        x3 = ((x1 + x2) + 2) >> 2
        b4 = (self._ac4 * (x3 + 32768)) >> 15
        b7 = (p_raw - b3) * (50000 >> self._os_mode)
        if (b7 < 0x80000000):
            p = (b7 * 2) / b4
        else:
            p = (b7 / b4) * 2
        x1 = p**2 >> 16
        x1 = (x1 * 3038) >> 16
        x2 = (-7357 * p) >> 16
        _pressure = (p + ((x1 + x2 + 3791) >> 4)) / 100.0
        
        return _pressure

    def sampleValues(self, valuetype=None):
        t_raw = self._readRawTemp()
        p_raw = self._readRawPressure()

        t = self._calcTemperature(t_raw)
        p = self._calcPressure(t_raw, p_raw)
        
        return [
            SensorEvent(self, t, 'C', 'temperature'),
            SensorEvent(self, p, 'Pa', 'pressure')
        ]


# 
# 
# 	def _updateAltitude(self):
# 		'''Calculates the altitude in meters.
# 		
# 		You need to call setSealevelPressure() before to set the current 
# 		sealevel pressure and get correct results.'''
# 		
# 		# Calculation taken straight from section 3.6 of the datasheet.
# 		pressure = float(self.getValue('pressure'))
# 		
# 		altitude = 44330.0 * (1.0 - pow(pressure / self._sealevel_pressure, (1.0 / 5.255)))
# 		self._logger.debug('Altitude {0} m'.format(altitude))
# 		
# 		self._setValue('altitude', altitude)
# 		
# 		return altitude
# 
# 
# 	def _updatePressureSealevel(self):
# 		'''Updates the pressure at sealevel.
# 		
# 		You need to call setAltitude() before to set the current altitide and
# 		get correct results.'''
# 		
# 		pressure = float(self.getValue('pressure'))
# 		p0 = pressure / pow(1.0 - self._current_altitude / 44330.0, 5.255)
# 		
# 		self._logger.debug('Sealevel pressure {0} Pa'.format(p0))
# 		
# 		self._setValue('pressure_sealevel', p0)
# 		
# 		return p0
# 
# 
# 	def setCurrentAltitude(self, height):
# 		self._current_altitude = height
# 		
# 		
# 	def setSealevelPressure(self, pressure):
# 		self._sealevel_pressure = pressure
# 		