from p24ip.login.decorators import must_be_logged, must_pick_device, must_be_logged_ajax, must_pick_device_ajax
from djangomako.shortcuts import render_to_response
from django.http import HttpResponse
from p24ip.device.models import Sensor
from p24ip.manage import get_struct
from __future__ import division

@must_be_logged
@must_pick_device
def control(request):
    from patelnia.p24 import PerDeviceRegistry
    r = PerDeviceRegistry(request.session['Device.dev_number'])
    if request.session['AccountDevice.privileges']==0:
        sensors = Sensor.objects.filter(Device=request.session['Device.id']).filter(canUserRead=True)
    else:
        sensors = Sensor.objects.filter(Device=request.session['Device.id'])
    return render_to_response('structures/rx910smartu1/control.html', {'request':request, 
                                                                       'registry':r,
                                                                        'sensors':sensors}) 
                                                      