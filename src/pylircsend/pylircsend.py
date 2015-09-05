
import array
from fcntl import ioctl
import os

from gencmds import get_cmd_data


dev_file='/dev/lirc0'

LIRC_SET_SEND_CARRIER = 13


def set_carrier(fd, freq):
    '''Set LIRC carrier frequency for sending.

    :param fd: File descriptor of lirc device file.
    :param freq: Carrier frequency to set.
    '''
    
    result = ioctl(fd, LIRC_SET_SEND_CARRIER, int(freq))

    if(result < 0):
        msg = "Failed to set carrier frequency to {0}Hz."
        logging.error(msg.format(freq))
        sys.exit(-1)
    else:
        msg = "Set carrier frequency to {0}Hz."
        logging.info(msg.format(freq))


def send_buffer(fd, data):
    
    retval = os.write(fd, buffer)
    
    if retval == len(buffer):
        msg = "Wrote {0} bytes of data to device."
        logging.info(msg.format(retval))
    else:
        msg = "Failed to write data completely to device (return value {0})."
        logging.error(msg.format(retval))


def main():

    fd = os.open(dev_file, os.O_RDWR)
    print('FD is {0}'.format(fd))

    set_carrier(fd, 38000)

    data = get_cmd_data()
    send_buffer(data)
    
    os.close(fd)


if __name__ == '__main__':
    main()
