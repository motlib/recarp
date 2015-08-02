'''Test code to read sensors and write results to a CSV file.'''


import time
import logging

from sensors.RPiInternalTemp import RPiInternalTemp


def main():
    '''Application entry point.'''
    
    logging.basicConfig(level=logging.DEBUG)

    # Create sensors array
    #TODO: should become some factory function.
    sensors = [
        RPiInternalTemp('rpi1')
    ]

    while True:
        values = []

        msg = 'Start sampling sensors.'
        logging.debug(msg)
        for s in sensors:
            msg = "Sampling sensor '{0}'."
            logging.info(msg.format(str(s)))
            values.extend(s.sampleValues())
            
        for v in values:
            msg = 'Sensor value: {0}'
            logging.info(msg.format(str(v)))
            
        msg = 'Sensor sampling completed. Sleeping until next cycle.'
        logging.debug(msg)
        
        time.sleep(2)

        
if __name__ == '__main__':
    main()
