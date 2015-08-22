# coding=UTF-8
from djangomako.shortcuts import render_to_response
from django.db.models import Min, Max
from p24ip.arch.models import ArchSensor    
    
def process(request, dfrom, dto):
    # Prepare reads
    
    archsensors = ArchSensor.objects.filter(Sensor__Device__id=request.session['Device.id'])
    
    sheets = {}
    
    for archsensor in archsensors:
        
        minimo = archsensor.read_set.filter(readed_on__lte=dto).filter(readed_on__gte=dfrom).exclude(data=None).order_by('data')[0]
        maximo = archsensor.read_set.filter(readed_on__lte=dto).filter(readed_on__gte=dfrom).exclude(data=None).order_by('-data')[0]
        
        sheets[archsensor.Sensor.name] = (minimo, maximo)
        
    return render_to_response('arch/sopmods/extrema.html',{'request':request,'reads':sheets})