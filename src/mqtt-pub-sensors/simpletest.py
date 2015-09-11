'''
Created on Mar 22, 2015

@author: andreas
'''

from sensors.BMP180 import BMP180
from sensors.HTU21D import HTU21D
from sensors.TSL2561 import TSL2561
from sensors.RPiInternalTemp import RPiInternalTemp
import time
import logging
import smbus 

def main():
    
    logging.basicConfig(level=logging.DEBUG)

    bus = smbus.SMBus(1)

    sensors = [ 
        BMP180('pr', bus), 
        HTU21D('rhum', 1), # other interface, needs bus number, not smbus object
        TSL2561('lum', bus),
        RPiInternalTemp('rpi1')
    ]
    
    while True:
        values = []
        
        for s in sensors:
            values.extend(s.sampleValue())
            
        for v in values:
            print(str(v))
            
        with open('log.csv', 'a') as f:
            data = '\t'.join([str(v.getValue()) for v in values])
            f.write('{0}\n'.format(data))
             
        time.sleep(2)
    
    

if __name__ == '__main__':
    main()