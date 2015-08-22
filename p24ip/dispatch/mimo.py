# coding=UTF-8
from p24ip.login.decorators import must_be_logged, must_pick_device, must_be_logged_ajax, must_pick_device_ajax
from djangomako.shortcuts import render_to_response
from django.http import HttpResponse
from p24ip.device.models import Sensor
from datetime import datetime
from p24ip.manage import get_struct
from __future__ import division
from p24ip.manage.models import Device
import simplejson as json
from patelnia.p24 import Device as P24Device
from patelnia.p24 import Sensor as P24Sensor
   
   
def process(request, dev_number):
    d = Device.objects.get(dev_number=int(dev_number))
    
    pd = P24Device(int(dev_number))
    pd.s1r4089.orderRead()
    pd.s1r4134.orderRead()
    pd.s1r4136.orderRead()
    pd.s1r4104.orderRead()
    
    external = Sensor.objects.get(Device=d, modbus_devid=1, regtype=0, register=4089)
    co = Sensor.objects.get(Device=d, modbus_devid=1, regtype=0, register=4134)
    internal = Sensor.objects.get(Device=d, modbus_devid=1, regtype=0, register=4136)
    cwu = Sensor.objects.get(Device=d, modbus_devid=1, regtype=0, register=4104)
    
    xr = HttpResponse(json.dumps([external.getLastRead()[0], internal.getLastRead()[0], cwu.getLastRead()[0], co.getLastRead()[0]]))
    xr['Pragma'] = 'no-cache'
    return xr 