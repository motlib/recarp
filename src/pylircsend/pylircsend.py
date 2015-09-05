
import array
from fcntl import ioctl
import os


dev_file='/dev/lirc0'

LIRC_SET_SEND_CARRIER = 13


def set_carrier(fd, freq):
    result = ioctl(fd, LIRC_SET_SEND_CARRIER, int(freq))

    if(result < 0):
        msg = "Failed to set carrier frequency to {0}Hz."
        logging.error(msg.format(freq))
        sys.exit(-1)
    else:
        msg = "Set carrier frequency to {0}Hz."
        logging.info(msg.format(freq))
    

def main():

    fd = os.open(dev_file, os.O_RDWR)
    print('FD is {0}'.format(fd))

    set_carrier(fd, 38000)

    
    os.close(fd)

    # a = array.array('I', [1,2,3,4]).tobytes()
    

if __name__ == '__main__':
    main()
