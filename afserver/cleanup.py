#! /usr/bin/python
# coding=UTF-8
'''Uruchamiane gdy serwer się wyłącza'''
from patelnia.p24 import enumDevices
from afruntime.device import Device
import os
from sys import exit

for x in enumDevices():
    Device(x.devid).setStat('thread.reader', 0)
    Device(x.devid).setStat('thread.handler', 0)
    Device(x.devid).setStat('online', 0)
exit(0)