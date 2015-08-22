from p24ip.login.decorators import must_be_logged, must_pick_device
from p24ip.manage.models import Device
from djangomako.shortcuts import render_to_response
from patelnia import p24
from p24ip.manage import get_struct
from afruntime.device import Device as AFDevice
@must_be_logged
@must_pick_device
def process(request):
    dev = Device.objects.get(id=request.session['Device.id'])
    xd = p24.Device(dev.dev_number)
    struct = get_struct(request)
    af = AFDevice(dev.dev_number)
    return render_to_response('device/overview.html', {'dev':dev,'request':request,
                                                       'vendor':xd.vendor,
                                                       'struct':struct,
                                                       'af':af})
    
    