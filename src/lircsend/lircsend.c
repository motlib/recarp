#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>/* open */
#include <unistd.h>/* exit */
#include <sys/ioctl.h>/* ioctl */
#include <stdint.h> /* uint32_t */

#include "lirc.h"
#include "gencmds.h"


#define DEVICE_FILE_NAME "/dev/lirc0"


/**
 * Set carrier frequency to 38kHz.
 */
static void set_carrier(int fd)
{
    uint32_t freq = 38000;
    int retval;

    retval = ioctl(fd, LIRC_SET_SEND_CARRIER, &freq);

    if(retval < 0)
    {
	printf("ioctl LIRC_SET_SEND_CARRIER failed: %d\n", retval);
	exit(-1);
    }
    else
      {
	printf("ioctl LIRC_SET_SEND_CARRIER succeeded.\n");
      }
}


/**
 * Write the signal data to the lirc device file.
 */
static void send_signal(int fd, cmd_info_t * cmdinfo)
{
    int retval;
    int count;

    printf("Writing %d bytes of data to device.\n", cmdinfo->size);

    count = cmdinfo->size / sizeof(int);
    if (cmdinfo->size % sizeof(int) || count % 2 == 0)
      {
	printf("ERROR: Wrong data size.\n");
	return;
      }


    retval = write(fd, cmdinfo->data, cmdinfo->size);

    if(retval < 0)
    {
      perror("Error:");
        printf("Writing data to device file failed: %d\n", retval);
    }
    else
    {
      printf("Result of write call: %d\n", retval);
    }

}


/**
 * Open the lirc device, set the carrier frequency and then send one
 * command.
 */
int main(int argc, char **argv)
{
    int fd;
    cmd_info_t cmd_info;
    int retval;

    fd = open(DEVICE_FILE_NAME, O_RDWR);

    if(fd < 0)
    {
	printf("Can't open device file: %s\n", DEVICE_FILE_NAME);
	exit(-1);
    }

    set_carrier(fd);

    /* Test to send signal with id 0. Later here the correct signal
     * data needs to be generated. */

    retval = gen_cmd(&cmd_info, 0);
    if(retval != 0)
    {
	perror("Failed to generate lirc signal data.\n");
	exit(-1);
    }
    
    send_signal(fd, &cmd_info);

    close(fd);
    
    return 0;
}
