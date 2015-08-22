# -*- coding: utf-8 -*-
'''Komunikacja MODBUS i kod Kolekcjonera Frisko'''
from __future__ import division
import struct
import socket
from threading import Thread
from threading import Timer
import datetime
import os

def lx(st):
    return '.'.join(map(lambda x: str(ord(x)), st))

class ModbusManager:
	def __init__(self):
		'''Przygotowuje tablice CRC'''
		lst = []
		i = 0
		while (i<256):
			data = i<<1
			crc = 0
			j = 8
			while (j>0):
				data >>= 1
				if ((data^crc)&0x1):
					crc = (crc>>1) ^ 0xA001
				else:
					crc >>= 1
				j -= 1
			lst.append (crc)
			i += 1
		self.table = lst
	def cCRC(self,st):
		'''Liczy MODBUS-CRC z podanego stringa'''
		crc = 0xFFFF
		for ch in st:
			crc = (crc>>8)^self.table[(crc^ord(ch))&0xFF]
		return struct.pack('<H',crc)

        def generateREAD_HOLDING(self, address, register):
            x = struct.pack('>BBHH',address, 3, register, 1)
            return x + self.cCRC(x)
        def generateWRITE_HOLDING(self, address, register, value):
            x = struct.pack('>BBHH',address, 6, register, value)
            return x + self.cCRC(x)
        def generateREAD_COIL(self, address, register):
            x = struct.pack('>BBHH', address, 1, register & 65528, 8)
            return x + self.cCRC(x)
        def generateWRITE_COIL(self, address, register, value):
            if value == 1:
                x = struct.pack('>BBHHBB', address, 5, register, 255, 0)
            else:
                x = struct.pack('>BBHHH', address, 5, register, 0)
            return x + self.cCRC(x)
        def parseREAD_HOLDING(self, data, address, register):
            assert self.cCRC(data[:-2]) == data[-2:], 'Wrong CRC'+lx(data)
            assert ord(data[1]) == 3, 'Wrong operation '+lx(data)
            return ord(data[3])*256 + ord(data[4])
        def parseREAD_COIL(self, data, address, register):
            treg = register & 65528
            assert self.cCRC(data[:-2]) == data[-2:], 'Wrong CRC'+lx(data)
            assert ord(data[1]) == 1, 'Wrong operation '+lx(data)
            par = ord(data[3])
            while treg < register:
                par = (par & 254) // 2
                treg += 1
            return (par & 1)

	def parseWRITE_HOLDING(self, data, address, register):
            assert self.cCRC(data[:-2]) == data[-2:], 'Wrong CRC'+lx(data)
            assert ord(data[1]) == 6, 'Wrong operation '+lx(data)
	def parseWRITE_COIL(self, data, address, register):
            assert self.cCRC(data[:-2]) == data[-2:], 'Wrong CRC'+lx(data)
            assert ord(data[1]) == 5, 'Wrong operation '+lx(data)
