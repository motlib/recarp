import logging

from pylis import PyLiS

class BitlistRemote(PyLiS):
    '''Base class for remotes having their own state coded in bits.'''
    
    def __init__(self, bitlength, device):
        super().__init__(device)
        
        self.data = [0] * bitlength
        
        self.bit_positions = {}
    
    
    def set_bit_positions(self, **positions):
        self.bit_positions.update(positions)
        
        
    def init_bitlist(self, data):
        if len(data) != len(self.data):
            raise ValueError('Bit data is not of same length.')
        
    
    def merge(self, pos, repl):
        i = 0

        for e in repl:
            self.data[pos] = e
            i += 1
            pos += 1

    
    def merge_data(self, pos_name, repl):
        pos = self.bit_positions[pos_name]
        self.merge(pos, repl)    

    
    def bitlist_to_int(self, bitlist):
        '''Convert a bitlist to integer. 
        
        Bitlist is expected in LSB format.'''
        
        out = 0
        
        for bit in reversed(bitlist):
            out = (out << 1) | bit
            
        return out


    def int_to_bitlist(self, val, list_len):
        '''Convert an integer to a bitlist of specified length.
        
        bitlist is generated in LSB format.'''
        
        bitlist = [0] * list_len
        
        bm = 1
        for bit in range(list_len):
            if val & bm != 0:
                bitlist[bit] = 1
            bm <<= 1

        return bitlist 


class Panasonic_A75C2665(BitlistRemote):
    '''Implementation of the Panasonic A75C2665 air conditioning remote control.
    '''
    
    def __init__(self, device='/dev/lirc0'):
        '''Initialize the remote control object. 
        
        :param string device: The lirc device file to open.'''
        
        super().__init__(bitlength=19*8, device=device)

        self.set_bit_positions(
            on_off=40,
            mode=44,
            temp=49,
            air_dir=64,
            fan_speed=68,
            checksum=144,
        )

        # 18 bytes plus 1 byte checksum as init data
        self.merge(0, [
            0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 
            0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 
            0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 
            1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 
            0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 
            0, 0, 0, 0, 0, 0, 0, 0, ])
        
        self.setup = {
            'on_off': 'on',
            'dir': 'auto',
            'vent': 'auto',
            'temp': 24,
            'mode': 'cool',
            }


    def set_power_status(self, status):
        '''Set the power status.
        
        :param string status: Either 'on' or 'off'.'''
        
        statuus = {
            'on': [1, ],
            'off': [0, ],
            }
        
        self.merge_data('on_off', statuus[status])


    def set_temperature(self, temp):
        '''Set the air temperature. 
        
        :param temp: The temperature in degree celsius.'''

        temp_list = self.int_to_bitlist(temp, 5)

        self.merge_data('temp', temp_list)


    def set_mode(self, mode):
        '''Set the operation mode.
        
        :param string mode: The operation mode. One of 'heat', 'cool', 'dry' 
          and 'auto'.'''
         
        modes = {
            'auto': [0, 0, 0],
            'heat': [0, 0, 1],
            'cool': [1, 1, 0],
            'dry': [0, 1, 0],
        }

        self.merge_data('mode', modes[mode])


    def set_air_dir(self, air_dir):
        '''Set air output direcion. '''
        dirs = {
            'auto': [1, 1, 1, 1],
            '1': [1, 0, 0, 0],
            '2': [0, 1, 0, 0],
            '3': [1, 1, 0, 0],
            '4': [0, 0, 1, 0],
            '5': [1, 0, 1, 0],
        }

        self.merge_data('air_dir', dirs[air_dir])


    def set_fan_speed(self, fan_speed):
        '''Set the fan speed. '''
        
        fan_speeds = {
            'auto': [0, 1, 0, 1],
            'high': [1, 1, 1, 0],
            'medium': [1, 0, 1, 0],
            'low': [1, 1, 0, 0],
        }

        self.merge_data('fan_speed', fan_speeds[fan_speed])


    def add_checksum(self):
        '''Calculate the checksum byte.
        
        The bytes in the bitlist are stored in LSB order.'''

        cs_range = range(
            0, 
            (int(len(self.data) / 8)) - 1)

        val = 0
        for bytepos in cs_range:
            bitpos = bytepos * 8 
            
            val += self.bitlist_to_int(
                self.data[bitpos:bitpos + 8])
        
        cs_list = self.int_to_bitlist(val, 8)
        
        self.merge_data('checksum', cs_list)


    def update_bitstring(self, **setup):
        logging.debug(setup)

        if 'mode' in setup.keys():
            self.set_mode(setup['mode'])
        
        if 'air_dir' in setup.keys():
            self.set_air_dir(setup['air_dir'])
        
        if 'fan' in setup.keys():
            self.set_fan_speed(setup['fan'])
            
        if 'temp' in setup.keys():
            self.set_temperature(setup['temp'])
            
        if 'power' in setup.keys():
            self.set_power_status(setup['power'])

        self.add_checksum()


    def generate_irdata(self, **setup):
        self.update_bitstring(**setup)
        
        # start the ir data with the preamble
        irdata = [3500, 1700]

        for c in self.data:
            # add the pulse
            irdata.append(460)
            
            # add the pause
            if c == 0:
                irdata.append(420)
            elif c == 1:
                irdata.append(1260)
            else:
                msg = "Invalid value '{0}' in bitlist."
                raise ValueError(msg.format(c))

        # add the suffix (last pulse)
        irdata.append(420)

        return irdata
