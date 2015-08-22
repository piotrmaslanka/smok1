from patelnia.p24 import Exceptions
from afruntime import DEVDB_ROOT
import os
import re
import codecs
from datetime import datetime
import afruntime.config
import lancero.client
from lancero.operators import Get
from afruntime.config import getRegistry
from afruntime.numeric import *
sensorRegexp = re.compile('s([0-9]+)([rfi])([0-9]+)')
reg_typeStI = {'r':0, 'f':1, 'i':2, 'o':3}
reg_typeItS = {0:'r', 1:'f', 2:'i', 3:'o'}

lancero.client.registerServer(lancero.client.ServerDefinitionEntry('127.0.0.1', getRegistry('afserver-lancero-port'), 'afserver', ''))
lancero.client.registerServer(lancero.client.ServerDefinitionEntry('127.0.0.1', getRegistry('afsensors-lancero-port'), 'afsensors', ''))
sObj = lancero.base.RemoteProxy(lancero.base.RemoteSource('afserver', 0))
afsObj = lancero.base.RemoteProxy(lancero.base.RemoteSource('afsensors', 0))
from afruntime.device import Device as AFDevice

class Sensor(object):
    __slots__ = ('device','modbus_nr','reg_type','register','intervals')
    def __init__(self, device, modbus_nr, reg_type, register, intervals=[]):
        self.device = device
        self.modbus_nr = modbus_nr
        self.reg_type = reg_type
        self.register = register
        self.intervals = intervals
    def getReadTime(self):
        x = reg_typeItS[self.reg_type]
        try:
            stat = os.stat(DEVDB_ROOT+str(self.device.devid)+'/'+str(self.modbus_nr)+x+str(self.register))
        except:
            raise Exceptions.NotReaded
        return datetime.fromtimestamp(stat[8])
    def write(self, value):
        value = inttouint(value)
        if not self.device.isOnline():
            raise Exceptions.DeviceOffline
        else:
            Get(sObj.write(self.device.devid, self.modbus_nr, self.reg_type, self.register, value))
    def orderRead(self):
        if not self.device.isOnline():
            raise Exceptions.DeviceOffline
        else:
            Get(sObj.read(self.device.devid, self.modbus_nr, self.reg_type, self.register))
    def getUpdatedRead(self, timeout):
        from patelnia.p24.Operations import UpdatedRead
        return UpdatedRead(self, timeout)
    def readFi(self):
        x = reg_typeItS[self.reg_type]
        try:
            f = open(DEVDB_ROOT+str(self.device.devid)+'/'+str(self.modbus_nr)+x+str(self.register),'r')
        except:
            raise Exceptions.NotReaded

        d = f.read().strip()
        if d[:5] == 'ERROR':
            raise Exceptions.ReadErrored
        return int(d)
        
    def __int__(self):
        return uinttoint(self.readFi())
        

class GlobalRegistry(object):
    __slots__ = ()
    
    def __delitem__(self, name):
        afruntime.config.delRegistry(name)
    def __getitem__(self, name):
        try:
            return afruntime.config.getRegistry(name)
        except:
            raise Exceptions.EntryNotExist(name)
        
    def __setitem__(self, name, value):
            return afruntime.config.setRegistry(name, value)
  
    def iteritems(self):
        for dir in os.listdir(DEVDB_ROOT+'REGISTRY/'):
            yield (dir, self[dir])

registry = GlobalRegistry()

class PerDeviceRegistry(object):
    __slots__ = ('devid',)
    def __init__(self, devid):
        self.devid = devid
        
    def iteritems(self):
        for dir in os.listdir(DEVDB_ROOT+str(self.devid)+'/REGISTRY/'):
            yield (dir, self[dir])
        
    def __getitem__(self, name):
        try:
            return AFDevice(self.devid).getRegistry(name)
        except:
            raise Exceptions.EntryNotExist(name)
        
    def __setitem__(self, name, value):
        return AFDevice(self.devid).setRegistry(name, value)
    def __delitem__(self, name):
        try:
            AFDevice(self.devid).delRegistry(name)
        except:
            raise Exceptions.EntryNotExist(name)
    
class Device(object):
    '''Single device registered within the system'''
    def __getattr__(self, name):
        if name == 'vendor':
            try:
                s = AFDevice(self.devid).getStat('vendor')
            except:
                raise Exceptions.NotReaded
            return s
        if name == 'structure':
            try:
                s = AFDevice(self.devid).getRegistry('structure')
            except:
                raise Exceptions.NotReaded
            return s
        if name == 'alerts':
            from patelnia.p24.Alert import AlertRegistry
            self.alerts = AlertRegistry(self.devid)
            return self.alerts
        m = sensorRegexp.match(name)
        if m != None:
            return Sensor(self, int(m.group(1)), reg_typeStI[m.group(2)], int(m.group(3)))
        raise AttributeError, name+' not defined'
    
    def __init__(self, devid):
        '''devid - device id of the device'''
        if not os.path.isdir(DEVDB_ROOT+str(devid)):
            raise Exceptions.DeviceNotExist(devid)
        self.devid = devid
        self.registry = PerDeviceRegistry(self.devid)
        
    def isOnline(self):
        '''Returns whether device is online'''
        try:
            return (AFDevice(self.devid).getStat('online') == 1)
        except:
            raise Exceptions.DatabaseFailure

    def signalFastreadRequired(self):
        try:
            Get(afsObj.fastRead(self.devid))
        except:
            raise Exceptions.DatabaseFailure

    def sleep(self, amount):
        try:
            Get(sObj.sleep(self.devid, amount))
        except:
            raise Exceptions.DatabaseFailure
    
    def reboot(self):
        try:
            Get(sObj.reboot(self.devid))
        except:
            raise Exceptions.DatabaseFailure

    def reread_sensorics(self):
        try:
            Get(afsObj.reread(self.devid))
        except:
            raise Exceptions.DatabaseFailure
        

def enumDevices():
    devs = []
    for entry in os.listdir(DEVDB_ROOT):
        try:
            int(entry)
        except:
            continue
        else:
            devs.append(Device(int(entry)))
    return devs