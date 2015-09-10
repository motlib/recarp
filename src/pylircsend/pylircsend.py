'''Control a infrared remote control transmitter supported by lirc.

Author: Andreas Schroeder <andreas@a-netz.de>
'''

from gencmds import Panasonic_A75C2665
import logging


def main():
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s', 
        level=logging.DEBUG)


    with Panasonic_A75C2665() as rc:
        rc.set_send_carrier(38000)
        
        setup = {
            'on_off': 'off',
            'dir': 'auto',
            'vent': 'high',
            'temp': 24,
            'mode': 'cool',
            }


        rc.

        # get / create command data and send it out
        data = get_cmd_data(setup)
        write_buffer(fd, data)
    
        

if __name__ == '__main__':
    main()
