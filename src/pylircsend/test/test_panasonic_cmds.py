'''
Created on Sep 11, 2015

@author: andreas
'''
import unittest

from remote_controls import Panasonic_A75C2665


class Test(unittest.TestCase):


    def test_cmds(self):
        self.maxDiff = None
        rc = Panasonic_A75C2665()
        
        s1 = '01000000000001000000011100100000000000000000110000001100000000011111010100000000000000000110000000000110000000000000000000000001000000000110000010000001'
        s1_list = [int(c) for c in s1]
        
        setup = {'on_off': 'off', 'temp': 24, 'mode':'cool', 'fan_speed': 'auto', 'air_dir': 'auto'}
        rc.update_bitstring(setup)
        
        res = ''.join(['{0}'.format(c) for c in rc.data])
        
        print('req', s1)
        print('ret', res)
        
        
        
        self.assertEqual(rc.data, s1_list)
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()