from patelnia.p24 import Exceptions
from datetime import datetime, timedelta
from time import sleep

class UpdatedRead(object):
    __slots__ = ('sensor','timeout','standby','lastReadTime')
    def __init__(self, sensor, timeout):
        self.sensor = sensor
        self.timeout = timeout
        self.standby = False
    def isReaded(self):
        try:
            self.sensor.getReadTime()
        except Exceptions.NotReaded:
            return False
        return True
    def loopUpdated(self):
        while self.willBeInvalidAfter(0):
            if not self.sensor.device.isOnline():
                raise Exceptions.DeviceOffline
            sleep(0.2)
    def loopReaded(self):
        while not self.isReaded():
            if not self.sensor.device.isOnline():
                raise Exceptions.DeviceOffline
            sleep(0.2)
    def __int__(self):
        try:
            if self.willBeInvalidAfter(0):
                if self.standby == True:
                    if self.lastReadTime == self.getReadTime():
                        return int(self.sensor)
                    else:
                        self.standby = False
                        return int(self)
                else:
                    self.lastReadTime = self.getReadTime()
                    self.orderRead()
                    self.standby = True
                    return int(self.sensor)
            else:
                self.standby = False
                return int(self.sensor)
        except Exceptions.NotReaded:
            self.sensor.orderRead()
            self.loopReaded()
    def willBeInvalidAfter(self, time):
        return (self.needsUpdateIn() <= timedelta(0, time))
    def orderRead(self):
        self.sensor.orderRead()
    def write(self, val):
        self.sensor.write(val)
    def getReadTime(self):
        return self.sensor.getReadTime()
    def getUpdatedRead(self, timeout):
        return self.sensor.getUpdatedRead(timeout)
    def needsUpdateIn(self):
        rt = self.sensor.getReadTime()
        tod = timedelta(0, self.timeout)
        rv = tod - (datetime.now() - rt)

        if rv > timedelta(0):
            return rv
        else:
            return timedelta(0)