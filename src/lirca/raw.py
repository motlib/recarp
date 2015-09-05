# coding: utf-8
import io
import os

import spur


class RawTimings():

    def __init__(self, raw):
        self.raw = raw
        self.cartesian = False
        self.tags = []

    @classmethod
    def from_file(cls, fname):
        """Factory method to create obj from file."""
        return RawTimings(read_raw_from_file(fname))

    @classmethod
    def from_folder(cls, fname):
        """Factory method to create dict of obj from files in given
        folder.
        """
        raw_dict = read_from_folder(fname)
        ret_dict = {}
        for key in raw_dict:
            data = RawTimings(raw_dict[key])
            data.tags = key.split('_')
            ret_dict[key] = data
        return ret_dict

    def _to_timing(self):
        y = 0
        for x in self.raw:
            y = 1 if y == 0 else 0
            yield (x, y)

    def _to_cartesian(self):
        x = 0
        yield (0, 1)
        for i, val in enumerate(self.raw):
            x += val
            yield (x, i % 2)

    @property
    def x(self):
        if self.cartesian:
            func = self._to_cartesian
        else:
            func = self._to_timing

        return [x for x, _ in func()]

    @property
    def y(self):
        if self.cartesian:
            func = self._to_cartesian
        else:
            func = self._to_timing

        return [y for _, y in func()]

    @property
    def on(self):
        return [x for x, y in self._to_timing() if y]

    @property
    def off(self):
        return [x for x, y in self._to_timing() if not y]

    @property
    def off_binary(self):
        return [int(int(x) > 700) for x in self.off]

    @property
    def off_binary_str(self):
        return ''.join([str(b) for b in self.off_binary])

    def off_binary_to_byte(self, start=0, num=None, reverse=False,
                           complement=False):
        if not num:
            stop = len(self.off_binary)
        else:
            stop = start + (num * 8)

        data_bytes = []
        for i in range(start, stop, 8):
            byte = self.off_binary_str[i:i + 8]
            if not byte:
                continue

            if reverse:
                byte = ''.join(reversed(byte))

            int_byte = int(byte, base=2)

            if complement:
                int_byte = ~int_byte

            data_bytes.append(int_byte)

        return data_bytes


def find_binary_in_string(string, num):
    idx = 0
    bin_str = bin(num)[2:]  # ignore leading '0b'
    while True:
        idx = string.find(bin_str, idx)
        if idx == -1:
            return
        yield idx
        idx += 1


def parse_raw_string(string):
    """Returns the LIRC raw valus as list without preceding time elapsed.

    Record message burst:
    .. code-block::
    sudo /etc/init.d/lirc stop
    mode2 -m -d /dev/lirc0 > ./on_20C_auto_auto.raw

    Returns:
        list: LIRC raw values (on/off timings, starting with on)
    """
    raw = string.split('\n')
    # ignore time elapsed between the recording start
    # and the arrival of the first IR signal
    raw = raw[2:]
    return ''.join(raw).split()


def read_raw_from_file(fname):
    """Read a LIRC raw message burst from fname

    Record message burst:
    .. code-block::
    sudo /etc/init.d/lirc stop
    mode2 -m -d /dev/lirc0 > ./on_20C_auto_auto.raw

    Returns:
        list: LIRC raw values (on/off timings, starting with on)
    """
    with open(fname) as fh:
        content = fh.read()
    return parse_raw_string(content)


def read_from_folder(folder):
    """Reads all LIRC raw message files from a folder and returns
    a dict over it with the filename as keys.

    Returns:
        dict: {filename: list_of_lirc_raw_timings}
    """

    raw_dict = dict()

    for file in os.listdir(folder):
        raw = read_raw_from_file(os.path.join(folder, file))
        raw_dict[file] = raw

    return raw_dict


def read_raw_from_ssh(hostname, username, password, dev='/dev/lirc0'):
    """Calls 'mode2' remote and returns the stdout output.

    Args:
        hostname (str): Remote device ip address
        username (str): ssh username
        password (str): ssh password
        dev (str): LIRC device path on remote device

    Returns:
        mode2 output in alternative display mode
    """
    shell = spur.SshShell(hostname,
                          username,
                          password,
                          missing_host_key=spur.ssh.MissingHostKey.accept)

    # capture raw data in alternative display mode
    cmd = ['mode2', '-m', '-d', dev]
    err = io.BytesIO()
    out = io.BytesIO()
    with shell:
        shell.spawn(cmd,
                    store_pid=True,
                    stdout=out,
                    stderr=err)

        # Return when something was written on stderr
        err_msg = err.getvalue().decode('utf-8')
        if err_msg:
            print('\nCommand failed: \n{0}'.format(err_msg))
            return None

        input('Press any key to stop capturing: ')

    return out.getvalue().decode('utf-8')
