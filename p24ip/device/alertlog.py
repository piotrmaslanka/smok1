# coding=UTF-8
from p24ip.login.decorators import must_be_logged, must_pick_device, must_be_service
from djangomako.shortcuts import render_to_response
from django.shortcuts import redirect
from patelnia.p24 import Device

@must_be_logged
@must_pick_device
@must_be_service
def process(request):
    
    d = Device(request.session['Device.dev_number'])
    a = d.alerts
    d.registry['alert'] = '0'
    return render_to_response('device/alertlog.html', {'request':request,
                                                       'alerts':a,
                                                       'severity':2})
    
@must_be_logged
@must_pick_device
@must_be_service
def yellow(request):
    
    d = Device(request.session['Device.dev_number'])
    a = d.alerts
    d.registry['alert'] = '0'
    return render_to_response('device/alertlog.html', {'request':request,
                                                       'alerts':a,
                                                       'severity':1})    

@must_be_logged
@must_pick_device
@must_be_service
def red(request):
    
    d = Device(request.session['Device.dev_number'])
    a = d.alerts
    d.registry['alert'] = '0'
    return render_to_response('device/alertlog.html', {'request':request,
                                                       'alerts':a,
                                                       'severity':1})        