from sensors.SensorBase import SensorBase, SensorEvent



class RPiInternalTemp(SensorBase):
    
    def __init__(self, sensor_name):
        SensorBase.__init__(self, 
            sensor_name=sensor_name)
        
        
    def sampleValues(self, valuetype=None):
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = int(f.read())
        
        temp = temp / 1000.0    
        
        return [
            SensorEvent(self, temp, 'C', 'temperature')
        ]