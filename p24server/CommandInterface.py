# coding=UTF-8
from Settings import DATABASE_ROOT
from Sensorics import fastRead, readSensorsFor
from Server.Connections import CONNECTIONS
from Server.P24.Orders import *
from thread import start_new_thread
import os
from time import sleep

import lancero.server
import os

class ManagingObject(object):
    def fastread(self, device_id):
        fastRead(device_id)
    def sleep(self, device_id, time):
        try:
            CONNECTIONS[device_id].orders.put(P24SleepOrder(time))
        except:
            pass
    def reboot(self, device_id):
        try:
            CONNECTIONS[device_id].orders.put(P24RebootOrder())
        except:
            pass
    def rereadSensorics(self, device_id):
        readSensorsFor(device_id)
    def read(self, device_id, modbus, regtype, register):
        try:
            CONNECTIONS[device_id].orders.put(P24ReadOrder(regtype, modbus, register))
        except:
            pass
    def write(self, device_id, modbus, regtype, register, value):
        try:
            CONNECTIONS[device_id].orders.put(P24WriteOrder(regtype, modbus, register, value))
        except:
            pass
    def getsettings(self, device_id):
        try:
            CONNECTIONS[device_id].orders.put(P24NetinfoSetOrder())
        except:
            pass
    def setsettings(self, ip, subnet, router, dns, target):
        try:
            CONNECTIONS[int(order[1])].orders.put(P24NetinfoSetOrder(ip,subnet,router,dns,target))
        except:
            pass

def initialize():
    '''Run CommandInterface'''
    z = ManagingObject()
    lancero.server.startServer(z, '127.0.0.1', 9000)
    while True:
        sleep(1000000)

def launch_demonize():      # odpala CommandInterface jako nowy wątek
    start_new_thread(initialize, ())