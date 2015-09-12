'''
Created on Sep 11, 2015

@author: andreas
'''
import unittest
from remote_controls import BitlistRemote

class TestBitlistRemote(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        
        self.bl = 24
        
        self.rc = BitlistRemote(bitlength=self.bl, device='/dev/lirc0')


    def test_bitlist_init(self):
        self.assertEqual(len(self.rc.data), self.bl)

        
    def test_bitlist_content(self):
        self.assertEqual(self.rc.data, [0] * self.bl)


    def test_bitlist_to_int(self):
        # empty list is 0
        self.assertEqual(self.rc.bitlist_to_int([]), 0)
        
        self.assertEqual(self.rc.bitlist_to_int([0]), 0)
        
        self.assertEqual(self.rc.bitlist_to_int([1]), 1)
        
        self.assertEqual(self.rc.bitlist_to_int([1,0]), 1)
        
        self.assertEqual(self.rc.bitlist_to_int([0,1]), 2)


    def test_int_to_bitlist(self):
        self.assertEqual(self.rc.int_to_bitlist(0, 1), [0])
        
        self.assertEqual(self.rc.int_to_bitlist(0, 2), [0, 0])
        
        self.assertEqual(self.rc.int_to_bitlist(1, 1), [1])
        
        self.assertEqual(self.rc.int_to_bitlist(6, 3), [0, 1, 1])
        
        self.assertEqual(self.rc.int_to_bitlist(6, 4), [0, 1, 1, 0])
        
        self.assertEqual(self.rc.int_to_bitlist(1, 2), [1, 0])
        
        self.assertEqual(self.rc.int_to_bitlist(16, 2), [0, 0])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()