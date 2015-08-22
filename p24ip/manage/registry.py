# coding=UTF-8
from p24ip.login.decorators import must_be_logged, must_pick_device, must_be_service
from djangomako.shortcuts import render_to_response
from django.shortcuts import redirect
from patelnia.p24 import GlobalRegistry

@must_be_logged
@must_pick_device
@must_be_service
def process(request):
    return render_to_response('manage/registry.html', {'request':request,
                                                       'registry':GlobalRegistry()})