# coding=UTF-8
from django.db import models
from django import forms
from djangomako.shortcuts import render_to_response
from p24ip.login.decorators import must_be_logged, must_pick_device, must_be_logged_ajax, must_pick_device_ajax
from p24ip.manage.models import Device
from p24ip.device.models import Sensor
from django.http import HttpResponse
import simplejson as json
from patelnia import p24

@must_be_logged
@must_pick_device
def display(request):
    if request.session['AccountDevice.privileges']==0:
        sensors = Sensor.objects.filter(Device=request.session['Device.id']).filter(canUserRead=True).order_by('sorting')
    else:
        sensors = Sensor.objects.filter(Device=request.session['Device.id']).order_by('sorting')
    return render_to_response('device/control.html', {'request':request, 'sensors':sensors})

@must_be_logged_ajax
@must_pick_device_ajax
def ajax(request):
    if request.GET['method']=='read':
        if request.session['AccountDevice.privileges']==0:
            sensors = Sensor.objects.filter(Device=request.session['Device.id']).filter(canUserRead=True)
        else:
            sensors = Sensor.objects.filter(Device=request.session['Device.id'])
        serdata = []
        for sensor in sensors:
            try:
                x,y = sensor.getLastRead()
            except:
                x = None
                y = None
            serdata.append((sensor.lsRepr(),x,str(y),))
        p24.Device(request.session['Device.dev_number']).signalFastreadRequired()
        return HttpResponse(json.dumps(serdata))    
    elif request.GET['method']=='write':
        sensor_id = int(request.GET['sid'])
        value = float(request.GET['value'])
        
        try:
            sensor = Sensor.objects.get(id=sensor_id)
        except:
            return HttpResponse('NO_SENSOR')
        
        if sensor.Device.id != request.session['Device.id']:
            return HttpResponse('INVALID_SENSOR')
        if (request.session['AccountDevice.privileges']==0) and (not sensor.canUserWrite):
            return HttpResponse('NO_PRIVILEGES')
        d = p24.Device(request.session['Device.dev_number'])
        s = p24.Sensor(d, sensor.modbus_devid, sensor.regtype, sensor.register)
        s.write(sensor.fromUserinput(value))
        d.sleep(1)
        s.orderRead()
        return HttpResponse('OK')
    else:
        return HttpResponse('WTF?')