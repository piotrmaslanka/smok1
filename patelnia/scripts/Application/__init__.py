from patelnia import p24
from datetime import datetime, timedelta
from patelnia.p24.Operations import UpdatedRead
from patelnia.p24.Exceptions import NotReaded, DeviceOffline
from threading import Thread, Lock
from time import sleep

class ApplicationExecutionThread(Thread):
    def __init__(self, app):
        Thread.__init__(self)
        self.app = app
    def run(self):
        self.app.run()
    def __del__(self):
        self.app.__dict__['lock'].release()

class Application(object):
    def run(self):
        while True:
                # Run all applications
            mxdelay = 99999999999999999
            try:
                self.__updateSensors(True)
                isOnline = self.device.isOnline()
                for app in self.apps:
                    if (app.NEEDS_ONLINE) and isOnline:
                        tmp = app.iteration(self)
                    elif not app.NEEDS_ONLINE:
                        tmp = app.iteration(self)
                    else:
                        continue
                    if tmp == None: continue
                    if tmp < mxdelay: mxdelay = tmp

                for name, value in self.__dict__.iteritems():
                    if type(value) == UpdatedRead:
                        tmp = value.needsUpdateIn()
                        tmp = tmp.days * 86400 + tmp.seconds
                        if tmp < mxdelay: mxdelay = tmp
            except:
                pass

            if mxdelay == 99999999999999999:
                mxdelay = 30    # Something is wrong.

            sleep(float(mxdelay))

    def __updateSensors(self, force=False):
        '''Orders to update UpdateReads'''
        for name, value in self.__dict__.iteritems():
            if type(value) == UpdatedRead:
                try:
                    if value.needsUpdateIn() == timedelta(0):
                        value.orderRead()
                        if force:
                            value.loopUpdated()
                        
                except NotReaded:
                    value.orderRead()
                    if force:
                        value.loopReaded()
    def _start(self):
        '''Starts executing the application. Will return False if locked'''
        if not self.lock.acquire():
            return False
        try:
            self.updateSensors(True)
        except:
            pass
        ApplicationExecutionThread(self).start()

class Sensor(object):
    __slots__ = ('modbus_nr','reg_type','register','timeout')
    def __init__(self, modbus_nr, reg_type, register, timeout=None):
        self.modbus_nr = modbus_nr
        self.reg_type = reg_type
        self.register = register
        self.timeout = timeout
    def returnSensor(self, device):
        if self.timeout == None:
            return p24.Sensor(device, self.modbus_nr, self.reg_type, self.register)
        else:
            return p24.Sensor(device, self.modbus_nr, self.reg_type, self.register).getUpdatedRead(self.timeout)

def returnModdedApplication(application, device):
    app = application()
    for name, value in application.__dict__.iteritems():
        if type(value) == Sensor:
            app.__dict__[name] = value.returnSensor(device)
    app.__dict__['device'] = device
    app.__dict__['lock'] = Lock()
    app.__dict__['apps'] = []
    app.init()
    return app