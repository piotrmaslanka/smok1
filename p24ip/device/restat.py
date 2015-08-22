from p24ip.login.decorators import must_be_logged, must_pick_device, must_be_service
from django.shortcuts import redirect
from p24ip.manage.models import Device
from afruntime.device import Device as AFDevice

@must_be_logged
@must_pick_device
def clearstats(request):
    if request.session['Account.privileges'] == 1:
        dev = Device.objects.get(id=request.session['Device.id'])
        af = AFDevice(dev.dev_number)
        af.setStat('transmission.successes', 0)
        af.setStat('transmission.errors', 0)
    return redirect('/device/overview/')

@must_be_logged
@must_pick_device
def errtoggle(request):
    if request.session['Account.privileges'] == 1:
        dev = Device.objects.get(id=request.session['Device.id'])
        af = AFDevice(dev.dev_number)
        af.setRegistry('correct.errors', not af.getRegistry('correct.errors'))
    return redirect('/device/overview/')