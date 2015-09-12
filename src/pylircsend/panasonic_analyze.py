'''Utility to analyze the output of the mode2 tool (part of lirc) according 
to the protocol for the Panasonic A75C2665 a/c remote control.

It will print a bit string according to the received and decoded data. ''' 


__author__ = 'Andreas <andreas@a-netz.de>'
__docformat__ = 'reStructuredText'


import sys


def main():
    file = sys.argv[1]
    
    print('{0}:'.format(file), end='')

    with open(file, 'r') as f:
        s = False
        c = 0

        for l in f:
            d = l.split(' ')
            t = d[0]
            v = int(d[1])
            c = c + 1
            
            if v > 8000 and c > 10:
                # recognize the start pattern: a 10000us pause
                s = True
                c = 0
                
            if s == True and c > 2 and t == 'pulse':
                # if start pattern has been seen, print a 1 / 0 if there is a 
                # pulse longer / shorter than ca. 800 (usually more then 
                # 1200 / less then 450
                if v > 800:
                    print('1', end='')
                else:
                    print('0', end='')

    print('')

if __name__ == '__main__':
    main()
