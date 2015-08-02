
import struct
import time
from sensors.SensorBase import SensorBase, SensorEvent
import fcntl
import io

# fcntl
_I2C_SLAVE = 0x0703

# Default I2C address
_DEFAULT_ADDRESS = 0x40

# Configuration parameters
RESOLUTION_12BITS      = 0b00000000
RESOLUTION_8BITS       = 0b00000001
RESOLUTION_10BITS      = 0b10000000
RESOLUTION_11BITS      = 0b10000001
# _END_OF_BATTERY        = 0b01000000
# _ENABLE_ONCHIP_HEATER  = 0b00000100
_DISABLE_ONCHIP_HEATER = 0b00000000
_ENABLE_OTP_RELOAD     = 0b00000000
_DISABLE_OTP_RELOAD    = 0b00000010
_RESERVED_BITMASK      = 0b00111000

# Commands
_CMD_TEMPERATURE  = '\xF3'
_CMD_HUMIDITY     = '\xF5'
_CMD_WRITE_CONFIG = '\xE6'
_CMD_READ_CONFIG  = '\xE7'
_CMD_SOFT_RESET   = '\xFE'

# Data bits specification
_STATUS_BITMASK     = 0b00000011
_STATUS_TEMPERATURE = 0b00000000
_STATUS_HUMIDITY    = 0b00000010
_STATUS_LSBMASK     = 0b11111100

class HTU21D(SensorBase):
    def __init__(self, sensor_name, bus, addr=_DEFAULT_ADDRESS):
        '''Initializes the sensor with some default values.

        bus: The SMBus descriptor on which this sensor is attached.
        addr: The I2C bus address
            (default is 0x40).

        '''
        
        SensorBase.__init__(
            self, 
            sensor_name=sensor_name)
        
        self._ior = io.open('/dev/i2c-' + str(bus), 'rb', buffering=0)
        self._iow = io.open('/dev/i2c-' + str(bus), 'wb', buffering=0)
        fcntl.ioctl(self._ior, _I2C_SLAVE, addr)
        fcntl.ioctl(self._iow, _I2C_SLAVE, addr)
        
        self._resolution = RESOLUTION_12BITS
        self._onchip_heater = _DISABLE_ONCHIP_HEATER
        self._otp_reload = _DISABLE_OTP_RELOAD

        self._use_temperature = True

        self._reset()
        self._reconfigure()

    @property
    def use_temperature(self):
        '''Returns whether to measure temperature or not.

        '''
        return (self._use_temperature)

    @use_temperature.setter
    def use_temperature(self, use_temperature):
        assert(use_temperature == True
               or use_temperature == False)
        self._use_temperature = use_temperature

    @property
    def resolution(self):
        '''Gets/Sets the resolution of temperature value.

        RESOLUTION_12BITS: RH 12 bits, Temp 14 bits.
        RESOLUTION_8BITS:  RH  8 bits, Temp 12 bits.
        RESOLUTION_10BITS: RH 10 bits, Temp 13 bits.
        RESOLUTION_11BITS: RH 11 bits, Temp 11 bits.

        '''
        return (self._resolution)

    @resolution.setter
    def resolution(self, resolution):
        assert(resolution == RESOLUTION_12BITS
               or resolution == RESOLUTION_8BITS
               or resolution == RESOLUTION_10BITS
               or resolution == RESOLUTION_11BITS)
        self._resolution = resolution
        self._reconfigure()

    def _reset(self):
        self._iow.write(_CMD_SOFT_RESET)
        time.sleep(0.02)

    def _reconfigure(self):
        self._iow.write(_CMD_READ_CONFIG)
        configs = self._ior.read(1)
        (config,) = struct.unpack('B', configs)
        config = ((config & _RESERVED_BITMASK)
                  | self._resolution
                  | self._onchip_heater
                  | self._otp_reload)
        self._iow.write(_CMD_WRITE_CONFIG + struct.pack('B', config))

    def sampleValues(self, valuetype=None):
        #vals = self._bus.read_i2c_block_data(
        #    self._address,
        #    _CMD_TEMPERATURE_HOLD, 
        #    3)
        
        self._iow.write(_CMD_TEMPERATURE)
        time.sleep(0.05)
        vals = self._ior.read(3)
        (temphigh, templow, crc) = struct.unpack('BBB', vals)
        temp = (temphigh << 8) | (templow & _STATUS_LSBMASK)
        _temperature = -46.85 + (175.72 * temp) / 2**16

        self._iow.write(_CMD_HUMIDITY)
        time.sleep(0.02)
        vals = self._ior.read(3)
        (humidhigh, humidlow, crc) = struct.unpack('BBB', vals)
        humid = (humidhigh << 8) | (humidlow & _STATUS_LSBMASK)
        _humidity = -6 + (125.0 * humid) / 2**16

        return [
            SensorEvent(self, _temperature, 'C', 'temperature'),
            SensorEvent(self, _humidity, '%RH', 'relative humidity'),
        ]
    

#     
#     def getCrc8(self, value):
#         "Calulate the CRC8 for the data received"
#         # Ported from Sparkfun Arduino HTU21D Library: https://github.com/sparkfun/HTU21D_Breakout
#         remainder = ( ( value[0] << 8 ) + value[1] ) << 8
#         remainder |= value[2]
#         
#         # POLYNOMIAL = 0x0131 = x^8 + x^5 + x^4 + 1
#         # divsor = 0x988000 is the 0x0131 polynomial shifted to farthest left of three bytes
#         divsor = 0x988000
#         
#         for i in range(0, 16):
#             if( remainder & 1 << (23 - i) ):
#                 remainder ^= divsor
# 
#             divsor = divsor >> 1
#         
#         return remainder
