# coding=UTF-8
from datetime import datetime
from thread import start_new_thread
from Settings import DATABASE_ROOT
from time import time, sleep
import os
from ConfigurationAdapter import getSensorsForDevice, writeReport, getAllDevices
from afruntime.device import Device

SENSORICS = {}

def readSensorsFor(id):     # Ponownie odczytuje sensorykę dla danego urządzenia
    SENSORICS[id] = []
       
    for descr in getSensorsForDevice(id):
       reading_path = str(id)+'/'+str(descr[2])
       if (descr[3] == 0):
           reading_path = reading_path+'r'
       elif (descr[3] == 1):
           reading_path = reading_path+'f'
       elif (descr[3] == 2):
           reading_path = reading_path+'i'
       reading_path = reading_path + str(descr[4])
       SENSORICS[id].append(Sensor(descr[0], reading_path, descr[6]))
    
def completeConfigReread():
    SENSORICS = {}    
    for dev_number in getAllDevices():
        readSensorsFor(dev_number[0])


class Sensor(object):
    '''Sensor, as seen by sensor processor'''
    def __init__(self, archid, reading_path, interval):
        self.reading_path = reading_path
        self.archid = archid
        self.lastupdated = time()
        self.interval = interval
    def weight(self):    # za ile sekund następny odpyt
        f = self.interval - (time()-self.lastupdated)
        if f<0:
            return 0
        else:
            return f
    def needUpdating(self): # czy muszę być odpytany
        return (time() > self.interval + self.lastupdated)
    def signalUpdated(self):
        self.lastupdated = time()
    def execute(self):      # wykonaj odpyt
        self.signalUpdated()
        try:
            x = open(DATABASE_ROOT+self.reading_path,'r')
            v = int(x.read())
            if v > 32767:
                v = 32768 - v
        except:
            v = None
        writeReport(self.archid, datetime.now(), v)

def runner():   # coś co odpytuje jak trza
    while True:
        min_time = 120
        for k,v in SENSORICS.iteritems():
            try:
                x = Device(k).getStat('online')
                if x == 0:
                    raise Exception
            except:
                continue
            
            for sensor in v:
                if sensor.needUpdating():
                    sensor.execute()
                if sensor.weight() < min_time:
                    min_time = sensor.weight()
        if min_time == 0:
            continue
        sleep(min_time)
        try:
            open(DATABASE_ROOT+'FORCE.REREAD.ARCH','r')
        except:
            pass
        else:
            os.unlink(DATABASE_ROOT+'FORCE.REREAD.ARCH')
            completeConfigReread()
    
def launch():
    while True:
        try:
            completeConfigReread()
            runner()
        except:
            pass
    
def launch_demonize():
    start_new_thread(launch, ())
    