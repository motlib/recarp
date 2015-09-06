'''Control a infrared remote control transmitter supported by lirc.

Author: Andreas Schroeder <andreas@a-netz.de>
'''

from gencmds import get_cmd_data
from pylis import PyLiS


class Panasonic_A75C2665(PyLiS):
    




def main():
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s', 
        level=logging.DEBUG)


    with PyLiS() as p:
        p.set_send_carrier(38000)
        
        setup = def_setup = {
            'on_off': 'off',
            'dir': 'auto',
            'vent': 'high',
            'temp': 24,
            'mode': 'cool',
            }


        # get / create command data and send it out
        data = get_cmd_data(setup)
        write_buffer(fd, data)
    
        

if __name__ == '__main__':
    main()
