#ifndef GENCMDS_H
#define GENCMDS_H


#include "lirc.h"


typedef struct
{
    /** Size of the returned data in bytes. */
    lirc_t size;

    /** Pointer to the lirc data. */
    lirc_t *data;
} cmd_info_t;


/**
 * Generate a command to send by lirc.
 */
int gen_cmd(cmd_info_t * cmd_info, int id);


#endif /* GENCMDS_H */
