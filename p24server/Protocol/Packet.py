# coding=UTF-8
from struct import pack, unpack
from socket import MSG_WAITALL

class BasePacket(object):
    '''Very basic packet. Supports word-sized size and rest is data'''
    def __init__(self):
        self.data = ''
    def reset(self):
        self.data = ''
        self.resetPointer()
    def addByte(self, data):
        self.data = self.data + pack("!B",data)
    def addWord(self, data):
        self.data = self.data + pack("!H",data)
    def addDword(self, data):
        self.data = self.data + pack("!L",data)
    def addString(self, data):
        self.data = self.data + pack("!B",len(data)) + data
    def __str__(self):
        return pack("!B",len(self.data)) + self.data

    def resetPointer(self):
        self.ptr = 0
    def getByte(self):
        self.ptr = self.ptr+1
        return unpack("!B",self.data[self.ptr-1])[0]
    def getWord(self):
        self.ptr = self.ptr+2
        return unpack("!H",self.data[self.ptr-2:self.ptr])[0]
    def getDword(self):
        self.ptr = self.ptr+4
        return unpack("!L",self.data[self.ptr-4:self.ptr])[0]
    def getString(self):
        slen = self.getByte()
        string = self.data[self.ptr:self.ptr+slen]
        self.ptr = self.ptr+slen
        return string
        
        
class RequestHandlerPacket(BasePacket):
    def __init__(self, request):
        super(RequestHandlerPacket, self).__init__()
        self.request = request
    def readInStrict(self, length):
        self.data = self.request.request.recv(length, MSG_WAITALL)
        self.resetPointer()
    def readIn(self):
        slen = unpack("<B", self.request.request.recv(1))[0]
        mydat = ''
        while len(mydat) < slen:
            mydat = mydat + self.request.request.recv(4096)
        self.data = mydat
        self.resetPointer()
    def writeOut(self):
        self.request.request.send(str(self))
        
    