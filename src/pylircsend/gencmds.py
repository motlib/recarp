

import array
import logging



cmd = [ 
    #3827, 1368, 1696, 921, 8746, 76, 1651, 1026, 729, 127, 756,
    #142, 746, 133, 739, 145, 737, 154, 732, 159, 733, 148, 752, 997,
    #740, 996, 762, 993, 732, 132, 750, 137, 766, 1011, 703, 155, 723,
    #159, 691, 201, 648, 256, 621, 250, 631, 261, 559, 332, 547, 337,
    #532, 361, 531, 380, 495, 362, 512, 371, 505, 418, 471, 382, 495,
    #386, 487, 402, 473, 435, 468, 398, 470, 415, 461, 420, 464, 433,
    #460, 419, 464, 463, 417, 423, 487, 412, 457, 477, 405, 424, 459,
    #420, 460, 433, 460, 426, 458, 1286, 457, 1282, 455, 482, 414, 432,
    #444, 446, 451, 408, 466, 418, 466, 


    #10076, 
    3505, 1700, 459, 421,
    462, 1278, 462, 416, 466, 429, 466, 448, 432, 420, 465, 433, 450,
    427, 464, 423, 460, 424, 457, 420, 467, 429, 478, 405, 465, 1271,
    464, 420, 489, 400, 471, 416, 466, 422, 459, 419, 497, 397, 463,
    420, 468, 1278, 456, 1280, 463, 1283, 461, 421, 463, 418, 467,
    1273, 463, 430, 467, 417, 464, 447, 447, 410, 461, 426, 472, 415,
    465, 491, 387, 422, 472, 421, 464, 420, 463, 419, 465, 424, 461,
    426, 466, 417, 464, 419, 467, 413, 465, 434, 464, 1276, 458, 1282,
    460, 426, 457, 427, 468, 414, 471, 414, 467, 1285, 452, 429, 466,
    1276, 461, 1280, 456, 419, 500, 394, 465, 420, 462, 422, 461, 419,
    464, 427, 466, 417, 467, 416, 472, 416, 490, 1260, 464, 1274, 463,
    1281, 461, 1278, 460, 1288, 458, 471, 461, 1231, 462, 416, 466,
    1283, 478, 403, 468, 417, 461, 421, 469, 420, 472, 418, 457, 424,
    462, 418, 467, 445, 453, 422, 460, 414, 485, 403, 462, 457, 434,
    419, 464, 418, 467, 418, 494, 396, 464, 423, 464, 1282, 470, 1268,
    455, 434, 462, 421, 472, 406, 465, 419, 491, 400, 470, 415, 464,
    419, 463, 420, 535, 358, 502, 381, 469, 1272, 465, 1277, 457, 430,
    478, 406, 461, 420, 465, 420, 465, 458, 431, 432, 447, 433, 456,
    421, 475, 414, 473, 410, 464, 421, 465, 433, 451, 427, 461, 423,
    468, 412, 465, 427, 457, 434, 470, 412, 465, 416, 460, 423, 462,
    430, 468, 420, 460, 418, 463, 421, 465, 1297, 455, 416, 461, 422,
    545, 334, 463, 429, 465, 421, 465, 423, 462, 417, 478, 414, 489,
    403, 463, 1276, 462, 1276, 455, 432, 462, 424, 461, 419, 469, 409,
    466, 431, 462, 1282, 481, 398, 464, 1278, 461, 428, 464, 423, 470,
    409, 468, 416, 465, 1274, 473,
]

positions = {
    't': 3,
    'on_off': 41,
    'mode': 45,
    'temp': 50,
    'dir': 65,
    'vent': 69,
    'checksum': 145,
}


def str_repl(s, pos_name, repl):
    start = positions[pos_name]

    return s[0:start - 1] + repl + s[start+len(repl)-1:]


def set_on_off(s, status):
    return str_repl(s, 'on_off', '1' if status == 'on' else '0')


def set_temp(s, temp):
    # TODO: Works from 16 degree up to 31 degree
    # get last 5 lsbs of temperature and reverse it
    stemp = bin(temp)[-5:][::-1]

    return str_repl(s, 'temp', stemp)


def set_mode(s, mode):
    modes = {
        '1': '000',
        '2': '001',
        'cool': '110',
        '4': '010',
    }

    return str_repl(s, 'mode', modes[mode])

def set_dir(s, dir):
    dirs = {
        'auto': '1111',
        '5': '1000',
        '4': '0010',
        '3': '1100',
        '2': '0100',
        '1': '1010',
        }

    return str_repl(s, 'dir', dirs[dir])

def set_vent(s, vent):
    vents = {
        'auto': '0101',
        'high': '1110',
        'med': '1010',
        'low': '1100',
        }

    return str_repl(s, 'vent', vents[vent])

def add_checksum(s):
    
    s1 = s[:144]

    l = [s1[i:i+8] for i in range(0, len(s1), 8)]

    v = 0
    for e in l:
        # reverse each base-2-number, convert to int and add to sum
        v += int(e[::-1], 2)

        logging.debug('CN is ' + bin(v)[-8:])

    # add this to make sure sum is more than 8 bits wide :-)
    v += 0b100000000

    # take 8 lsb from sum, reverse string
    checksum = bin(v)[-8:][::-1]

    logging.info('CS is ' + checksum)

    s = str_repl(s, 'checksum', checksum)

    return s


def_setup = {
    'on_off': 'on',
    'dir': 'auto',
    'vent': 'auto',
    'temp': 24,
    'mode': 'cool',
}

def gen_bitstring(setup=def_setup):
    s = '01000000000001000000011100100000000000000000110000001100000000011111010100000000000000000110000000000110000000000000000000000001000000000110000000000000'
 
    logging.debug(setup)

    logging.debug('TE is ' + s)
   
    s = set_mode(s, setup['mode'])
    s = set_dir(s, setup['dir'])
    s = set_vent(s, setup['vent'])
    s = set_temp(s, setup['temp'])
    s = set_on_off(s, setup['on_off'])

    logging.debug('BS is ' + s)
    
    s = add_checksum(s)

    logging.debug('CS is ' + s)


    #s = ''.join([('1' if e > 1000 else '0') for e in l])
    return s
                

def gen_from_bitstring(str):
    

    if len(str) != 152:
        raise ValueError('Invalid telegram length.')

    data = [3500, 1700]

    for c in str:
        data.append(460)
        if c == '0':
            data.append(420)
        elif c == '1':
            data.append(1260)
        else:
            raise ValueError('Unsupported charater in string.')

    data.append(420)

    return data


def get_cmd_data(setup=def_setup):

    bstr = gen_bitstring(setup)
     
    data = gen_from_bitstring(bstr)

    a = array.array('I', data)
        
    return a.tobytes()
        

if __name__=='__main__':
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s', 
        level=logging.DEBUG)

    print(gen_bitstring())
