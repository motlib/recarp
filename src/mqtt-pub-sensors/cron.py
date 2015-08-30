
'''Running a cron-like schedule for reading sensors. 

Based on an idea from http://stackoverflow.com/questions/373335/how-do-i-get-a-cron-like-scheduler-in-python
'''

from datetime import datetime, timedelta
import time

# Some utility classes / functions first
class AllMatch(set):
    """Universal set - match everything"""
    def __contains__(self, item): return True
    
    allMatch = AllMatch()


# The actual Event class
class Event(object):
    def __init__(self, action, sec=allMatch, min=allMatch, hour=allMatch):
        self.secs = self.conv_to_set(sec)
        self.mins = self.conv_to_set(min)
        self.hours= self.conv_to_set(hour)
        self.action = action

        
    def conv_to_set(obj):  # Allow single integer to be provided
        if isinstance(obj, (int, long)):
            return set([obj])  # Single item
        if not isinstance(obj, set):
            obj = set(obj)
        return obj

    
    def matchtime(self, t):
        """Return True if this event should trigger at the specified datetime"""
        return ((t.second in self.seconds) and
            (t.minute     in self.mins) and
            (t.hour       in self.hours) and
            (t.day        in self.days) and
            (t.month      in self.months) and
            (t.weekday()  in self.dow))

    
    def check(self, t):
        if self.matchtime(t):
            self.action(*self.args, **self.kwargs)

            
class CronTab(object):
    def __init__(self, *events):
        self.events = events

    def run(self):
        
        while True:
            for e in self.events:
                e.check(t)
                
            time.sleep(0.5)
                    
