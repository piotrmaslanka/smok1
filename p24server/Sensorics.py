# coding=UTF-8
from datetime import datetime
from thread import start_new_thread
from threading import Lock
from time import time, sleep
from Server.Connections import CONNECTIONS
from Server.P24.Orders import *
from Server.P24.FileWriter import writeRunlevel
from Settings import DATABASE_ROOT

SENSORICS = {}

class Sensor(object):
    '''Sensor, as seen by sensor processor'''
    def __init__(self, id, regtype, dev, register, runlevel_settings):
        self.id = id
        self.lastupdated = time()
        self.dev = dev
        self.regtype = regtype
        self.register = register
        self.runlevel_settings = runlevel_settings
        try:
            self.advanceToRunlevel(CONNECTIONS[self.id].runlevel)
        except:
            pass
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
    def advanceToRunlevel(self, runlevel):
        self.signalUpdated()
        try:
            self.interval = self.runlevel_settings[runlevel]
        except:
            pass
    def execute(self):      # wykonaj odpyt
        self.signalUpdated()
        CONNECTIONS[self.id].orders.put(P24ReadOrder(self.regtype, self.dev, self.register))

SENSORICS_QUERY_LOCK = Lock()

def clearSensorsFor(id):
    SENSORICS_QUERY_LOCK.acquire()
    del SENSORICS[id]
    SENSORICS_QUERY_LOCK.release()

def runner():   # coś co odpytuje jak trza
    while True:
        SENSORICS_QUERY_LOCK.acquire()
        min_time = 30
        for k,v in SENSORICS.iteritems():
            for sensor in v:
                if sensor.needUpdating():
                    sensor.execute()
                if sensor.weight() < min_time:
                    min_time = sensor.weight()
        SENSORICS_QUERY_LOCK.release()                    
        sleep(min_time)
        
def launch():
    try:
        runner()
        try:
            SENSORICS_QUERY_LOCK.release()
        except:
            pass
        
    except Exception, e:
        pass
    
def launch_demonize():
    start_new_thread(launch, ())

def umfastRead(id):
    SENSORICS_QUERY_LOCK.acquire()
    try:
        sidsensors = SENSORICS[id]
        CONNECTIONS[id].runlevel = 0
        for sensor in sidsensors:
            sensor.advanceToRunlevel(0)
    except:
        pass
    SENSORICS_QUERY_LOCK.release()

def fastRead(id):
    SENSORICS_QUERY_LOCK.acquire()
    
    try:
        sidsensors = SENSORICS[id]
        CONNECTIONS[id].rlvl1lastreported = datetime.now()
        if CONNECTIONS[id].runlevel == 1:
            raise Exception, 'Everything is OK despite the exception'
        CONNECTIONS[id].runlevel = 1
        for sensor in sidsensors:
            sensor.advanceToRunlevel(1)
    except:
        pass
    SENSORICS_QUERY_LOCK.release()
        
    
def readSensorsFor(id):     # Ponownie odczytuje sensorykę dla danego urządzenia
    SENSORICS_QUERY_LOCK.acquire()
    SENSORICS[id] = []

    try:
        config = open(DATABASE_ROOT + '/' + str(id) + '/CONFIG', 'r')
            
        for line in config.readlines():
           elems = line.split(' ')
           try:
               elems = map(lambda x: int(x), elems)
           except:
               continue
           sensor = Sensor(id, elems[1], elems[0], elems[2], elems[3:])
           crl = CONNECTIONS[id].runlevel
           sensor.advanceToRunlevel(crl)
           SENSORICS[id].append(sensor)
    except:
        pass
    SENSORICS_QUERY_LOCK.release()