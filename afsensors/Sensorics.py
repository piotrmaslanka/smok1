# coding=UTF-8
from afruntime import DEVDB_ROOT
from afruntime.config import getRegistry
from afruntime.device import Device
from datetime import datetime, timedelta
from threading import Lock
from time import time, sleep
import lancero.client
import lancero.base
from afruntime.log import log as debugLog
from lancero.operators import Get

lancero.client.registerServer(lancero.client.ServerDefinitionEntry('127.0.0.1', getRegistry('afserver-lancero-port'), 'afserver', ''))
sObj = lancero.base.RemoteProxy(lancero.base.RemoteSource('afserver', 0))


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
        self.rt1expire = None
        self.interval = self.runlevel_settings[0]
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
        if self.interval == self.runlevel_settings[runlevel]:
            print debugLog('Skipped runlevel change as there is no change in timer')
            return
        debugLog('ATR advancing to '+str(runlevel)+' with '+str(self.runlevel_settings[runlevel]))
        self.interval = self.runlevel_settings[runlevel]
    def execute(self):      # wykonaj odpyt
        self.signalUpdated()
        try:
            Get(sObj.read(self.id, self.dev, self.regtype, self.register))
        except:
            debugLog('ASK FAILED')

        if self.rt1expire != None:
            if datetime.now() > self.rt1expire:
                self.advanceToRunlevel(0)
                self.rt1expire = None

SENSORICS_QUERY_LOCK = Lock()

def clearSensorsFor(id):
    SENSORICS_QUERY_LOCK.acquire()
    try:
        del SENSORICS[id]
    except:
        pass
    SENSORICS_QUERY_LOCK.release()

def run():   # coś co odpytuje jak trza
    while True:
        SENSORICS_QUERY_LOCK.acquire()
        min_time = 30
        for k, v in SENSORICS.iteritems():
            for sensor in v:
                if sensor.needUpdating():
                    sensor.execute()
                if sensor.weight() < min_time:
                    min_time = sensor.weight()
        SENSORICS_QUERY_LOCK.release()
        sleep(min_time)

def fastRead(id):
    SENSORICS_QUERY_LOCK.acquire()
    try:
        sidsensors = SENSORICS[id]
        Device(id).setStat('runlevel1.lastreported', datetime.now())
        Device(id).setStat('runlevel', 1)
        for sensor in sidsensors:
            sensor.rt1expire = datetime.now() + timedelta(0, 15)
            sensor.advanceToRunlevel(1)
    except Exception, e:
        debugLog(str(e))

    
    SENSORICS_QUERY_LOCK.release()


def readSensorsFor(id):     # Ponownie odczytuje sensorykę dla danego urządzenia
    SENSORICS_QUERY_LOCK.acquire()
    SENSORICS[id] = []

    try:
        config = open(DEVDB_ROOT + '/' + str(id) + '/CONFIG', 'r')

        for line in config.readlines():
           elems = line.split(' ')
           try:
               elems = map(lambda x: int(x), elems)
           except:
               continue
           sensor = Sensor(id, elems[1], elems[0], elems[2], elems[3:])
           SENSORICS[id].append(sensor)
    except:
        pass
    SENSORICS_QUERY_LOCK.release()