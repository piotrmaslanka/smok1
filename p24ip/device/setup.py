from p24ip.login.decorators import must_be_logged, must_pick_device, must_be_service
from p24ip.device.models import Sensor, SensorForm
from djangomako.shortcuts import render_to_response
from django.shortcuts import redirect
from p24ip.manage.models import Device
from django.views.decorators.cache import cache_page

@must_be_logged
@must_pick_device
@must_be_service
def sensors_list(request):
    sensors = Sensor.objects.filter(Device=request.session['Device.id']).order_by('sorting')
    return render_to_response('device/setup.sensors_list.html', {'request':request, 'sensors':sensors})

@must_be_logged
@must_pick_device
@must_be_service
def sensor_delete(request, sensor_id):
    app = Sensor.objects.get(id=sensor_id)
    if app.Device.id != request.session['Device.id']:
        return redirect('/manage/pick/')
    app.delete()
    return redirect('/device/sensors/setup/list/')

@must_be_logged
@must_pick_device
@must_be_service
def sensor_edit(request, sensor_id):
    app = Sensor.objects.get(id=sensor_id)
    if app.Device.id != request.session['Device.id']:
        return redirect('/manage/pick/')
    af = SensorForm(instance=app)    
    if request.method == "POST":
        af = SensorForm(request.POST, instance=app)
        if af.is_valid():
            af.save()
            return render_to_response('device/setup.sensor_edit.html', {'request':request,
                                                                                 'form':af,
                                                                                'saved':True})    
    try:
        af
    except:
        af = SensorForm()
        
    return render_to_response('device/setup.sensor_edit.html', {'request':request,
                                                                         'form':af,
                                                                         'saved':False})
@must_be_logged
@must_pick_device
@must_be_service
def sensor_new(request):
    af = SensorForm()    
    if request.method == "POST":
        af = SensorForm(request.POST)
        af.instance.Device = Device.objects.get(id=request.session['Device.id'])
        if af.is_valid():
            af.save()
            return render_to_response('device/setup.sensor_new.html', {'request':request,
                                                                                 'form':af,
                                                                                'saved':True})    
    try:
        af
    except:
        af = SensorForm()
        
    return render_to_response('device/setup.sensor_new.html', {'request':request,
                                                                         'form':af,
                                                                         'saved':False})
sensor_new = cache_page(sensor_new, 60 * 60 * 24 * 7)


@must_be_logged
@must_pick_device
@must_be_service    
def save(request):
    from afruntime import DEVDB_ROOT
    from patelnia.p24 import Device
    sensors = Sensor.objects.filter(Device=request.session['Device.id'])
    xie = open(DEVDB_ROOT+str(request.session['Device.dev_number'])+'/CONFIG', 'w')
    for sensor in sensors:
        xie.write(str(sensor.modbus_devid)+" ")
        xie.write(str(sensor.regtype)+" ")
        xie.write(str(sensor.register)+" ")
        xie.write(str(sensor.interval_0)+" ")
        xie.write(str(sensor.interval_1)+"\n")
    del xie
    Device(request.session['Device.dev_number']).reread_sensorics()
    return render_to_response('device/setup.save.html', {'request':request})