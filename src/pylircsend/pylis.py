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
        '''Open the lirc device file.
        
        If it was already opened, it will be closed first and then opened 
        again.'''
        
        if self.fd != None:
            self.close()

        # open the dev_file file
        self.fd = os.open(self.dev_file, os.O_RDWR)
        
        if self.fd < 0:
            msg = "Failed to open dev_file file descriptor: {0}"
            logging.error(msg.format(self.fd))
            self.fd = None

        
    def close(self):
        '''Close the lirc device file if it was opened.'''
        if self.fd != None:
            # close the dev_file file
            os.close(self.fd)
            self.fd = None
            
            
    def is_open(self):
        '''Return true if the lirc device is currently opened.'''
        
        return (self.fd != None)
            

    def __enter__(self):
        '''Context-manager function to start using the lirc device resource.'''
        self.open()

        return self


    def __exit__(self, exc_type, value, traceback):
        '''Context-manager function to end using the lirc device resource.'''
        self.close()


    def set_send_carrier(self, freq):
        '''Set LIRC carrier frequency for sending.
        
        :param fd: File descriptor of lirc dev_file file.
        :param freq: Carrier frequency to set.'''
        
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


    def send_irdata(self, ir_data):
        '''Write a data ir_data to the dev_file.

        :param fd: The file descriptor to write to.  
        :param ir_data: The ir_data containing the data to send. The
          data consists of a list of integer values as expected by the
          lirc dev_file.'''

        if not self.is_open():
            raise Exception('Call to open() is missing.')

        # convert data list to byte stream
        byte_data = array.array('I', ir_data).tobytes()
        
        retval = os.write(self.fd, byte_data)
    
        if retval == len(byte_data):
            msg = "Successfully wrote {len} bytes of data to '{dev}'."
            logging.debug(msg.format(
                len=retval, 
                dev=self.dev_file))
        else:
            msg = "Failed to write data completely to '{dev}'. Return value {ret}."
            raise Exception(msg.format(
                ret=retval, 
                dev=self.dev_file))


    def generate_irdata(self):
        '''Abstract method to generate irdata list.'''
        
        raise Exception('Needs to be overriden in subclass.')


    def send_ir_command(self, **setup):
        ir_data = self.generate_irdata(**setup)
        self.send_irdata(ir_data)
        
        