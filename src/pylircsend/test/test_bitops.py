'''
Created on Sep 11, 2015

@author: andreas
'''
import unittest
from remote_controls import Panasonic_A75C2665

class Test(unittest.TestCase):


    def test_bitlist_to_int(self):
        rc = Panasonic_A75C2665()
        
        # empty list is 0
        self.assertEqual(rc.bitlist_to_int([]), 0)
        
        self.assertEqual(rc.bitlist_to_int([0]), 0)
        
        self.assertEqual(rc.bitlist_to_int([1]), 1)
        
        self.assertEqual(rc.bitlist_to_int([1,0]), 1)
        
        self.assertEqual(rc.bitlist_to_int([0,1]), 2)


    def test_int_to_bitlist(self):
        rc = Panasonic_A75C2665()
        
        self.assertEqual(rc.int_to_bitlist(0, 1), [0])
        
        self.assertEqual(rc.int_to_bitlist(0, 2), [0, 0])
        
        self.assertEqual(rc.int_to_bitlist(1, 1), [1])
        
        self.assertEqual(rc.int_to_bitlist(6, 3), [0, 1, 1])
        
        self.assertEqual(rc.int_to_bitlist(6, 4), [0, 1, 1, 0])
        
        self.assertEqual(rc.int_to_bitlist(1, 2), [1, 0])
        
        self.assertEqual(rc.int_to_bitlist(16, 2), [0, 0])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()