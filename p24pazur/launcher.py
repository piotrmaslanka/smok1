from threading import Thread
from patelnia.p24 import enumDevices, Device
from patelnia.scripts.Application import returnModdedApplication

class LauncherThread(Thread):
    devices = {}
    def run(self):
        for device in enumDevices():
            devid = device.devid
            struc = device.structure
            appmod = eval('__import__(\'structures.'+struc+'\').'+struc)
            try:
                if appmod.DONTRUN:
                    print 'Will not run '+str(devid)+' struct '+str(struc)+' due to DONTRUN'
                    continue
            except:
                pass
            self.devices[devid] = returnModdedApplication(appmod.MyApplication, device)
            
        for devid, application in self.devices.iteritems():
            print 'Starting '+str(Device(devid).structure)+' for '+str(devid)
            application._start()
                    