import array
import logging

from pylis import PyLiS


class Panasonic_A75C2665(PyLiS):
    
    def __init__(self, device='/dev/lirc0'):
        super(device)

        self.positions = {
            't': 3,
            'on_off': 41,
            'mode': 45,
            'temp': 50,
            'dir': 65,
            'vent': 69,
            'checksum': 145,
            }

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
        

        def str_repl(s, pos_name, repl):

            pos = self.positions[pos_name]
            i = 0

            for e in repl:
                self.bit_data[pos] = repl[i]
                i += 1
                pos += 1



        def set_on_off(s, status):
            statuus = {
                'on': [1, ],
                'off': [0, ],
                }
            str_repl(s, 'on_off', statuus[status])


        def set_temp(s, temp):
            # TODO: Works from 16 degree up to 31 degree
            # get last 5 lsbs of temperature and reverse it

            # generate string of bits
            stemp = bin(temp)[-5:][::-1]

            # generate list from string
            ltemp = [int(b) for b in stemp]

            self.str_repl(s, 'temp', ltemp)


        def set_mode(s, mode):
            modes = {
                '1': [0, 0, 0],
                '2': [0, 0, 1],
                'cool': [1, 1, 0],
                '4': [0, 1, 0],
                }

            self.str_repl(s, 'mode', modes[mode])

        def set_dir(s, dir):
            dirs = {
                'auto': [1, 1, 1, 1],
                '5': [1, 0, 0, 0],
                '4': [0, 0, 1, 0],
                '3': [1, 1, 0, 0],
                '2': [0, 1, 0, 0],
                '1': [1, 0, 1, 0],
                }

            self.str_repl(s, 'dir', dirs[dir])

        def set_vent(s, vent):
            vents = {
                'auto': [0, 1, 0, 1],
                'high': [1, 1, 1, 0],
                'med': [1, 0, 1, 0],
                'low': [1, 1, 0, 0],
                }

            self.str_repl(s, 'vent', vents[vent])

        def add_checksum(s):
    
            s1 = s[:144]

            l = [s1[i:i+8] for i in range(0, len(s1), 8)]

            v = 0
            for e in l:
                # reverse each base-2-number, convert to int and add to sum
                v += int(e[::-1], 2)
                
                logging.debug('CN is ' + bin(v)[-8:])

            # add this to make sure sum is more than 8 bits wide :-)
            v += 0b100000000

            # take 8 lsb from sum, reverse string
            checksum = bin(v)[-8:][::-1]

            logging.info('CS is ' + checksum)

            s = str_repl(s, 'checksum', checksum)

            return s


        def_setup = {
            'on_off': 'on',
            'dir': 'auto',
            'vent': 'auto',
            'temp': 24,
            'mode': 'cool',
            }

        def gen_bitstring(setup=def_setup):
            s = '01000000000001000000011100100000000000000000110000001100000000011111010100000000000000000110000000000110000000000000000000000001000000000110000000000000'
 
            logging.debug(setup)

            logging.debug('TE is ' + s)
   
            self.set_mode(setup['mode'])
            self.set_dir(setup['dir'])
            self.set_vent(setup['vent'])
            self.set_temp(setup['temp'])
            self.set_on_off(setup['on_off'])
            
            logging.debug('BS is ' + s)
    
            self.add_checksum()

            logging.debug('CS is ' + s)


        def gen_value_list(self):
    

            if len(self.bit_data) != 152:
                raise ValueError('Invalid telegram length.')

            irdata = [3500, 1700]

            for c in self.bit_data:
                irdata.append(460)
                if c == '0':
                    irdata.append(420)
                elif c == '1':
                    irdata.append(1260)
                else:
                    raise ValueError('Unsupported value in bitstring.')

            irdata.append(420)

            return irdata


    def get_cmd_data(setup=def_setup):

        bstr = gen_bitstring(setup)
     
        data = gen_from_bitstring(bstr)

        a = array.array('I', data)
        
        return a.tobytes()
        




if __name__=='__main__':
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s', 
        level=logging.DEBUG)

    print(gen_bitstring())
