#include "gencmds.h"

#include <stdio.h>
#include "lirc.h"

/* 
 * Command data is a simple sequence of integers. The sequence must
 * begin and end with a pulse timing. This means a sequence always has
 * an odd number of elements.  Numbers as printed from mode2 command
 * can directly be used as send data.
 */
static lirc_t cmd_26[] = {
#include "cmds/panasonic_a75c2665/2-26a.in"
};

static lirc_t cmd_28[] = {
#include "cmds/panasonic_a75c2665/2-28.in"
};

int gen_cmd(cmd_info_t * cmd_info, int id)
{
    if(id == 0)
    {
      printf("Providing dummy cmd.\n");
	cmd_info->size = sizeof(cmd_26);
	cmd_info->data = cmd_26;
    }
    else
    {
	cmd_info->size = sizeof(cmd_28);
	cmd_info->data = cmd_28;
    }

    return 0;
}
