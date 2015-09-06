'''
Author: Andreas <andreas@a-netz.de>
'''

import array
from fcntl import ioctl
import os
import logging
import struct


# ioctl code taken from lirc.h
LIRC_SET_SEND_CARRIER = 0x40046913

class PyLiS():
    '''Base class for sending infrared commands by use of a lirc
    device.'''

    def __init__(self, device='/dev/lirc0'):
        self.device = device
        self.fd = None


    def open(self):
        if self.fd != None:
            self.close()

        # open the device file
        self.fd = os.open(dev_file, os.O_RDWR)
        
        if self.fd < 0:
            msg = "Failed to open device file descriptor: {0}"
            logging.error(msg.format(fd))

        
    def close(self):
        if self.fd != None:
            # close the device file
            os.close(self.fd)
            self.fd = None
            

    def __enter__(self):
        self.open()

        return self


    def __exit__(self, exc_type, value, traceback):
        self.close()


    def set_send_carrier(self, freq):
        '''Set LIRC carrier frequency for sending.
        
        :param fd: File descriptor of lirc device file.
        :param freq: Carrier frequency to set.
        '''
        
        if self.fd == None:
            raise Exception('Call to open() is missing.')

        freqdata = struct.pack('I', freq)
        
        resdata = ioctl(self.fd, 0x40046913, freqdata)
        
        result = struct.unpack('I', resdata)[0]

        if(result < 0):
            msg = "Failed to set carrier frequency to {0}Hz."
            logging.error(msg.format(freq))
            sys.exit(-1)
        else:
            msg = "Set carrier frequency to {0}Hz."
            logging.info(msg.format(freq))


    def send_buffer(self, fd, buffer):
        '''Write a data buffer to the device.

        :param fd: The file descriptor to write to.  

        :param buffer: The buffer containing the data to send. The
          data consists of a list of integer values as expected by the
          lirc device.
        '''

        if self.fd == None:
            raise Exception('Call to open() is missing.')

        # convert data list to byte stream
        dar = array.array('I', buffer)
        
        retval = os.write(self.fd, dar.tobytes())
    
        if retval == len(buffer):
            msg = "Wrote {0} bytes of data to device."
            logging.debug(msg.format(retval))
        else:
            msg = "Failed to write data completely to device (return value {0})."
            logging.error(msg.format(retval))
