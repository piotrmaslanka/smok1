# coding=UTF-8
from afruntime.server import donothing
from afruntime.config import getRegistry
import lancero.server
from Sensorics import clearSensorsFor, readSensorsFor, fastRead
from afruntime.log import log as debugLog

class ManagingObject(object):
    def online(self, id):
        debugLog('Online for '+str(id))
        readSensorsFor(id)
    def reread(self, id):
        debugLog('Reread for '+str(id))
        readSensorsFor(id)
    def offline(self, id):
        debugLog('Offline for '+str(id))
        clearSensorsFor(id)
    def fastRead(self, id):
        debugLog('Fastread for '+str(id))
        fastRead(id)

def run():
    '''Run CommandInterface'''
    z = ManagingObject()
    lancero.server.startServer(z, '127.0.0.1', getRegistry('afsensors-lancero-port'))
    print 'LANCERO started'
    donothing()