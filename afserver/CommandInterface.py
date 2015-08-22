# coding=UTF-8
from afruntime.server import donothing
from afruntime.config import getRegistry
import lancero.server
from Order import *
from Connections import CONNECTIONS

class ManagingObject(object):
    def read(self, id, address, regtype, register):
        CONNECTIONS[id].orders.put(ReadOrder(address, regtype, register))
    def write(self, id, address, regtype, register, value):
        CONNECTIONS[id].orders.put(WriteOrder(address, regtype, register, value))
    def sleep(self, id, seconds):
        try:
            CONNECTIONS[id].orders.put(SleepOrder(seconds))
        except:
            return False
        return True
    def reboot(self, id):
        try:
            CONNECTIONS[id].orders.put(RebootOrder(seconds))
        except:
            return False
        return True

def run():
    '''Run CommandInterface'''
    z = ManagingObject()
    lancero.server.startServer(z, '127.0.0.1', getRegistry('afserver-lancero-port'))
    print 'LANCERO started'
    donothing()