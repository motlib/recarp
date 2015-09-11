import logging

from pylis import PyLiS


class Panasonic_A75C2665(PyLiS):
    
    def __init__(self, device='/dev/lirc0'):
        super().__init__(device)

        self.bit_positions = {
            #'t': 3,
            'on_off': 40,
            'mode': 44,
            'temp': 49,
            'air_dir': 64,
            'fan_speed': 68,
            'checksum': 144,
            }

        # 18 bytes plus 1 byte checksum
        self.data = [
            0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 
            0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 
            0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 
            1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 
            0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 
            0, 0, 0, 0, 0, 0, 0, 0, ]
        

    def merge_data(self, pos_name, repl):

        pos = self.bit_positions[pos_name]
        i = 0

        for e in repl:
            self.data[pos] = e
            i += 1
            pos += 1


    def set_on_off(self, status):
        statuus = {
            'on': [1, ],
            'off': [0, ],
            }
        self.merge_data('on_off', statuus[status])


    def set_temp(self, temp):
        '''Set the air temperature. '''
        # TODO: Works from 16 degree up to 31 degree
        # get last 5 lsbs of temperature and reverse it

        temp_list = self.int_to_bitlist(temp, 5)

        self.merge_data('temp', temp_list)


    def set_mode(self, mode):
        '''Set the operation mode (cool, heat, dry).
        
        :param string mode: The operation mode.
        '''
         
        modes = {
            '1': [0, 0, 0],
            '2': [0, 0, 1],
            'cool': [1, 1, 0],
            '4': [0, 1, 0],
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


    def add_checksum(self):
        # bytes in list are stored lsb first!

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

 
    def_setup = {
        'on_off': 'on',
        'dir': 'auto',
        'vent': 'auto',
        'temp': 24,
        'mode': 'cool',
        }


    def update_bitstring(self, setup=def_setup):
        logging.debug(setup)

        self.set_mode(setup['mode'])
        self.set_air_dir(setup['air_dir'])
        self.set_fan_speed(setup['fan_speed'])
        self.set_temp(setup['temp'])
        self.set_on_off(setup['on_off'])

        self.add_checksum()


    def generate_irdata(self, setup=def_setup):
        self.update_bitstring(setup)
        
        # start the ir data with the preamble
        irdata = [3500, 1700]

        for c in self.bit_data:
            # add the pulse
            irdata.append(460)
            
            # add the pause
            if c == '0':
                irdata.append(420)
            elif c == '1':
                irdata.append(1260)
            else:
                raise ValueError('Unsupported value in bitstring.')

        # add the suffix (last pulse)
        irdata.append(420)

        return irdata
    
        
if __name__=='__main__':
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s', 
        level=logging.DEBUG)

