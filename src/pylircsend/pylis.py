'''
Author: Andreas <andreas@a-netz.de>
'''

import array
from fcntl import ioctl
import os
import logging
import struct
import sys


# ioctl code taken from lirc.h
LIRC_SET_SEND_CARRIER = 0x40046913

class PyLiS(object):
    '''Base class for sending infrared commands by use of a lirc
    dev_file.'''

    def __init__(self, device='/dev/lirc0'):
        self.dev_file = device
        self.fd = None


    def open(self):
        if self.fd != None:
            self.close()

        # open the dev_file file
        self.fd = os.open(self.dev_file, os.O_RDWR)
        
        if self.fd < 0:
            msg = "Failed to open dev_file file descriptor: {0}"
            logging.error(msg.format(self.fd))
            self.fd = None

        
    def close(self):
        if self.fd != None:
            # close the dev_file file
            os.close(self.fd)
            self.fd = None
            
    def is_open(self):
        return (self.fd != None)
            

    def __enter__(self):
        self.open()

        return self


    def __exit__(self, exc_type, value, traceback):
        self.close()


    def set_send_carrier(self, freq):
        '''Set LIRC carrier frequency for sending.
        
        :param fd: File descriptor of lirc dev_file file.
        :param freq: Carrier frequency to set.
        '''
        
        if not self.is_open():
            raise Exception('Call to open() is missing.')

        freqdata = struct.pack('I', freq)
        
        resdata = ioctl(self.fd, LIRC_SET_SEND_CARRIER, freqdata)
        
        result = struct.unpack('I', resdata)[0]

        if(result < 0):
            msg = "Failed to set carrier frequency to {0}Hz."
            logging.error(msg.format(freq))
            sys.exit(-1)
        else:
            msg = "Set carrier frequency to {0}Hz."
            logging.info(msg.format(freq))


    def send_buffer(self, fd, rc_data):
        '''Write a data rc_data to the dev_file.

        :param fd: The file descriptor to write to.  

        :param rc_data: The rc_data containing the data to send. The
          data consists of a list of integer values as expected by the
          lirc dev_file.
        '''

        if self.fd == None:
            raise Exception('Call to open() is missing.')

        # convert data list to byte stream
        dar = array.array('I', rc_data)
        
        retval = os.write(self.fd, dar.tobytes())
    
        if retval == len(rc_data):
            msg = "Wrote {0} bytes of data to dev_file."
            logging.debug(msg.format(retval))
        else:
            msg = "Failed to write data completely to dev_file (return value {0})."
            logging.error(msg.format(retval))
