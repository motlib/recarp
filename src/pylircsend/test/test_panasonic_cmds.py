'''
Created on Sep 11, 2015

@author: andreas
'''

import unittest
import logging

from remote_controls import Panasonic_A75C2665


class TestPanasonicA75C2665(unittest.TestCase):

    setups = [
        { # 0
            'on_off': 'off', 'temp': 24, 'mode':'cool', 'fan_speed': 'auto', 'air_dir': 'auto',
            'expect': '0100000000000100000001110010000000000000 0 000 110 00 00011 0000000001 1111 0101 000000000000000001100000000001100000000000000000000000010000000001100000 10000001'
        }, 
        { # 1
            'on_off': 'on', 'temp': 24, 'mode':'cool', 'fan_speed': 'auto', 'air_dir': 'auto',
            'expect': '0100000000000100000001110010000000000000 1 000 110 00 00011 0000000001 1111 0101 000000000000000001100000000001100000000000000000000000010000000001100000 01000001',
        },
        { # 2
            'on_off': 'on', 'temp': 25, 'mode':'cool', 'fan_speed': 'auto', 'air_dir': 'auto',
            'expect': '0100000000000100000001110010000000000000 1 000 110 00 10011 0000000001 1111 0101 000000000000000001100000000001100000000000000000000000010000000001100000 00100001',
        },
        { # 3
            'on_off': 'on', 'temp': 25, 'mode':'cool', 'fan_speed': 'high', 'air_dir': 'auto',
            'expect': '0100000000000100000001110010000000000000 1 000 110 00 10011 0000000001 1111 1110 000000000000000001100000000001100000000000000000000000010000000001100000 00101010',
        },
        { # 4
            'on_off': 'on', 'temp': 25, 'mode':'cool', 'fan_speed': 'high', 'air_dir': '1',
            'expect': '0100000000000100000001110010000000000000 1 000 110 00 10011 0000000001 1000 1110 000000000000000001100000000001100000000000000000000000010000000001100000 01100010',
        },
        { # 5 
            'on_off': 'on', 'temp': 25, 'mode':'cool', 'fan_speed': 'high', 'air_dir': '5',
            'expect': '0100000000000100000001110010000000000000 1 000 110 00 10011 0000000001 1010 1110 000000000000000001100000000001100000000000000000000000010000000001100000 01010010',
        },
        { # 6
            'on_off': 'on', 'temp': 25, 'mode':'cool', 'fan_speed': 'high', 'air_dir': '3',
            'expect': '0100000000000100000001110010000000000000 1 000 110 00 10011 0000000001 1100 1110 000000000000000001100000000001100000000000000000000000010000000001100000 00010010',
        },
        { # 7
            'on_off': 'on', 'temp': 25, 'mode':'cool', 'fan_speed': 'high', 'air_dir': '4',
            'expect': '0100000000000100000001110010000000000000 1 000 110 00 10011 0000000001 0010 1110 000000000000000001100000000001100000000000000000000000010000000001100000 10010010',
        },
        { # 8
            'on_off': 'on', 'temp': 25, 'mode':'cool', 'fan_speed': 'high', 'air_dir': '2',
            'expect': '0100000000000100000001110010000000000000 1 000 110 00 10011 0000000001 0100 1110 000000000000000001100000000001100000000000000000000000010000000001100000 11100010',
        },
        { # 9
            'on_off': 'on', 'temp': 25, 'mode':'cool', 'fan_speed': 'low', 'air_dir': 'auto',
            'expect': '0100000000000100000001110010000000000000 1 000 110 00 10011 0000000001 1111 1100 000000000000000001100000000001100000000000000000000000010000000001100000 00101000',
        },
        { # 10
            'on_off': 'on', 'temp': 25, 'mode':'cool', 'fan_speed': 'medium', 'air_dir': 'auto',
            'expect': '0100000000000100000001110010000000000000 1 000 110 00 10011 0000000001 1111 1010 000000000000000001100000000001100000000000000000000000010000000001100000 00101100',
        },
        { # 11 - does not work. temperature wrong. in mode 1 not relevant?
            'on_off': 'on', 'temp': 26, 'mode':'1', 'fan_speed': 'auto', 'air_dir': 'auto',
            'expect': '0100000000000100000001110010000000000000 1 000 000 00 00001 1100000001 1111 0101 000000000000000001100000000001100000000000000000000000010000000001100000 01000000',
        },
        { # 12
            'on_off': 'on', 'temp': 26, 'mode':'2', 'fan_speed': 'auto', 'air_dir': 'auto',
            'expect': '0100000000000100000001110010000000000000 1 000 001 00 01011 0000000001 1111 0101 000000000000000001100000000001100000000000000000000000010000000001100000 01101001',
        },
        { # 13
            'on_off': 'on', 'temp': 26, 'mode':'cool', 'fan_speed': 'high', 'air_dir': 'auto',
            'expect': '0100000000000100000001110010000000000000 1 000 110 00 01011 0000000001 1111 1110 000000000000000001100000000001100000000000000000000000010000000001100000 01101010',
        },
        { # 14
            'on_off': 'on', 'temp': 26, 'mode':'4', 'fan_speed': 'auto', 'air_dir': 'auto',
            'expect': '0100000000000100000001110010000000000000 1 000 010 00 00011 0000000001 1111 0101 000000000000000001100000000001100000000000000000000000010000000001100000 01001110',
        },
        { # 15
            'on_off': 'on', 'temp': 26, 'mode':'cool', 'fan_speed': 'high', 'air_dir': 'auto',
            'expect': '0100000000000100000001110010000000000000 1 000 110 00 01011 0000000001 1111 1110 000000000000000001100000000001100000000000000000000000010000000001100000 01101010',
        }
    ]

    def setUp(self):
        unittest.TestCase.setUp(self)
        
        self.maxDiff = None

        self.rc = Panasonic_A75C2665()


    def test_cmd_1(self):
        self.run_cmd(1)


    def test_cmd_2(self):
        self.run_cmd(2)


    def test_cmd_3(self):
        self.run_cmd(3)


    def test_cmd_4(self):
        self.run_cmd(4)


    def test_cmd_5(self):
        self.run_cmd(5)


    def test_cmd_6(self):
        self.run_cmd(6)


    def test_cmd_7(self):
        self.run_cmd(7)


    def test_cmd_8(self):
        self.run_cmd(8)


    def test_cmd_9(self):
        self.run_cmd(9)


    def test_cmd_10(self):
        self.run_cmd(10)


    #def test_cmd_11(self):
    #    self.run_cmd(11)


    def test_cmd_12(self):
        self.run_cmd(12)


    def test_cmd_13(self):
        self.run_cmd(13)


    #def test_cmd_14(self):
    #    self.run_cmd(14)


    def test_cmd_15(self):
        self.run_cmd(15)
        

    def run_cmd(self, test_id):
        setup = TestPanasonicA75C2665.setups[test_id]
        
        s = setup['expect'].replace(' ', '')
        s1_list = [int(c) for c in s]
    
        self.rc.update_bitstring(**setup)
    
        res = ''.join(['{0}'.format(c) for c in self.rc.data])
    
        logging.debug('expected: {0}'.format(s))
        logging.debug('returned: {0}'.format(res))
    
        self.assertEqual(self.rc.data, s1_list)
    
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()