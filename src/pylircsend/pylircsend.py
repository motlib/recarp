'''Control a infrared remote control transmitter supported by lirc.

Author: Andreas Schroeder <andreas@a-netz.de>
'''

import array
from fcntl import ioctl, fcntl
import os
import logging
import struct
from gencmds import get_cmd_data


dev_file='/dev/lirc0'

# ioctl code taken from lirc.h
LIRC_SET_SEND_CARRIER = 0x40046913


def set_carrier(fd, freq):
    '''Set LIRC carrier frequency for sending.

    :param fd: File descriptor of lirc device file.
    :param freq: Carrier frequency to set.
    '''
    
    
    freqdata = struct.pack('I', freq)

    #freq = int(freq)
    resdata = ioctl(fd, 0x40046913, freqdata)

    result = struct.unpack('I', resdata)[0]

    if(result < 0):
        msg = "Failed to set carrier frequency to {0}Hz."
        logging.error(msg.format(freq))
        sys.exit(-1)
    else:
        msg = "Set carrier frequency to {0}Hz."
        logging.info(msg.format(freq))


def write_buffer(fd, buffer):
    '''Write a data buffer to the device.

    :param fd: The file descriptor to write to.
    :param buffer: The buffer containing the data to send. The
      structure of the data depends on the device file you are writing
      to.'''

    retval = os.write(fd, buffer)
    
    if retval == len(buffer):
        msg = "Wrote {0} bytes of data to device."
        logging.debug(msg.format(retval))
    else:
        msg = "Failed to write data completely to device (return value {0})."
        logging.error(msg.format(retval))


def main():
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s', 
        level=logging.DEBUG)


    

    try:
        # open the device file
        fd = os.open(dev_file, os.O_RDWR)

        # set carrier frequency. Usually 36 or 38kHz
        set_carrier(fd, 38000)

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
    
    finally:
        # close the device file
        os.close(fd)
        

if __name__ == '__main__':
    main()
