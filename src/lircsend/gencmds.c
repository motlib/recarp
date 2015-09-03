#include "gencmds.h"

#include "lirc.h"

static lirc_t cmd_26[] = {
#include "cmds/panasonic_a75c2665/2-26.in"
};

static lirc_t cmd_28[] = {
#include "cmds/panasonic_a75c2665/2-28.in"
};


int gen_cmd(cmd_info_t * cmd_info, int id)
{
    if(id == 0)
    {
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
