from socket import AF_INET, SOCK_STREAM, socket, SOL_TCP, TCP_NODELAY, SOL_SOCKET, SO_KEEPALIVE
from afruntime.log import log as debugLog
from datetime import datetime, timedelta
from time import sleep
from Socks import readin_strict
from struct import pack
from Modbus import ModbusManager
from __future__ import division

class MoteClass(object):
    def __init__(self, id, ip, port):
        self.id = id
        self.ip = ip
        self.port = port
        self.modbus = ModbusManager()

    def connectTibbo(self):
        self.sTibbo = socket(AF_INET, SOCK_STREAM)
        self.sTibbo.connect((self.ip, self.port))
        self.sTibbo.setsockopt(SOL_TCP, TCP_NODELAY, 1)
        self.sTibbo.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 0)
        self.sTibbo.setblocking(1)
        self.sTibbo.settimeout(60)

    def connectSelf(self):
        self.sServer = socket(AF_INET, SOCK_STREAM)
        self.sServer.connect(('127.0.0.1', 2405))
        self.sServer.setsockopt(SOL_TCP, TCP_NODELAY, 1)
        self.sServer.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 0)
        self.sServer.setblocking(1)
        self.sServer.settimeout(60)

    def readpacket_server(self):
        dt = ord(readin_strict(self.sServer, 1))
        return readin_strict(self.sServer, dt)

    def run(self):
        self.connectTibbo()
        self.connectSelf()
        self.sServer.send(pack('!L', self.id)+'\x00\x00\x00\xFF'+'\x00\x00\x00\x00')
        dat = readin_strict(self.sServer, 2)
        if dat != '\x01\x00':
            raise Exception, 'No 1-0 combo'
        while True:
            data = self.readpacket_server()
            if data[0] == '\x03':           # GET HOLDING RET ERROR
                register = ord(data[1])*256 + ord(data[2])
                modbus = ord(data[3])
                dat = self.modbus.generateREAD_HOLDING(modbus, register)
                self.sTibbo.send(dat)
                sdt = readin_strict(self.sTibbo, 7)
                val = self.modbus.parseREAD_HOLDING(sdt, modbus, register)
                self.sServer.send('\x03\x00'+ chr(val // 256) + chr(val & 255))
            elif data[0] == '\x04':           # GET COIL RET ERROR
                register = ord(data[1])*256 + ord(data[2])
                modbus = ord(data[3])
                dat = self.modbus.generateREAD_COIL(modbus, register)
                self.sTibbo.send(dat)
                sdt = readin_strict(self.sTibbo, 6)
                val = self.modbus.parseREAD_COIL(sdt, modbus, register)
                self.sServer.send('\x02\x00'+ chr(val))
            elif data[0] == '\x05':           # WRITE HOLDING
                register = ord(data[1])*256 + ord(data[2])
                value = ord(data[3])*256 + ord(data[4])
                address = ord(data[5])
                dat = self.modbus.generateWRITE_HOLDING(address, register, value)
                self.sTibbo.send(dat)
                sdt = readin_strict(self.sTibbo, 8)
                self.modbus.parseWRITE_HOLDING(sdt, address, register)
                self.sServer.send('\x02\x00\x00')
                readin_strict(self.sTibbo, 1)
            elif data[0] == '\x06':           # WRITE COIL
                register = ord(data[1])*256 + ord(data[2])
                value = ord(data[3])
                address = ord(data[4])
                dat = self.modbus.generateWRITE_COIL(address, register, value)
                self.sTibbo.send(dat)
                sdt = readin_strict(self.sTibbo, 8)
                self.modbus.parseWRITE_COIL(sdt, address, register)
                self.sServer.send('\x02\x00\x00')
                readin_strict(self.sTibbo, 1)
            else:
                raise Exception, 'Invalid data recv'

def start(id, ip, port):
    while True:
        try:
            debugLog('Start MOTE at ID='+str(id)+' IP='+str(ip)+' PORT='+str(port))
            x = MoteClass(id, ip, port)
            x.run()
        except Exception, e:
            debugLog('AFMOTEMOTE> Exception '+str(e)+' at mote '+str(id))
        del x
        sleep(60)