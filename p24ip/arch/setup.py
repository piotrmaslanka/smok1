from p24ip.login.decorators import must_be_logged, must_pick_device, must_be_service
from p24ip.manage.models import Device
from p24ip.device.models import Sensor
from p24ip.arch.models import ArchSensor
from django.shortcuts import redirect
from djangomako.shortcuts import render_to_response

@must_be_logged
@must_pick_device
@must_be_service
def makeArch(request, sensor_id):
    try:
        sensor = Sensor.objects.get(id=sensor_id)
    except:
        return redirect('/manage/pick/')

    if sensor.Device.id != request.session['Device.id']:
        return redirect('/manage/pick/')
    
    asr = ArchSensor()
    asr.Sensor = sensor
    asr.save()

    return redirect('/device/sensors/setup/list/')
    
@must_be_logged
@must_pick_device
@must_be_service    
def unmakeArch(request, sensor_id):
    try:
        asr = ArchSensor.objects.get(Sensor__id=sensor_id)
    except:
        return redirect('/manage/pick/')
    
    if asr.Sensor.Device.id != request.session['Device.id']:
        return redirect('/manage/pick/')
    
    asr.delete()
    return redirect('/device/sensors/setup/list/')
    
@must_be_logged
@must_pick_device
@must_be_service
def storeArchSettings(request):
    from afruntime import DEVDB_ROOT
    open(DEVDB_ROOT+'FORCE.REREAD.ARCH','w')
    return redirect('/device/sensors/setup/list/')