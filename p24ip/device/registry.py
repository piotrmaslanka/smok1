# coding=UTF-8
from p24ip.login.decorators import must_be_logged, must_pick_device, must_be_service
from djangomako.shortcuts import render_to_response
from django.shortcuts import redirect
from patelnia.p24 import Device

@must_be_logged
@must_pick_device
@must_be_service
def process(request):
    return render_to_response('device/registry.html', {'request':request,
                                                            'registry':Device(request.session['Device.dev_number']).registry})