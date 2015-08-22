# coding=UTF-8
from __future__ import division
from p24ip.manage.models import Device
from django.db import models
from django import forms

SENSOR_REGTYPE = ((0, u'Rejestr'),
                  (1, u'Flaga'),
                  (2, u'Wejście analogowe'),)

SENSOR_DATATYPE = ((0, 'Nominalny'),
                   (1, 'Temperatura(rejestr)'),
                   (2, 'Temperatura(rejestr) U2'))

SENSOR_ESEMANTIC = ((0, 'Brak'),
                    (1, 'Frisko'),
                    )

def negate(v):
    x = 0
    p = 32768
    while p <> 0:
       if (v & p == 0):
           x += p
       p = p//2
    return x

class Sensor(models.Model):
    Device = models.ForeignKey(Device)
    name = models.CharField(max_length=30, verbose_name=u'Opis')
    modbus_devid = models.IntegerField(verbose_name=u'ID urządzenia MODBUS')
    regtype = models.IntegerField(choices=SENSOR_REGTYPE, verbose_name=u'Typ rejestru')
    register = models.IntegerField(verbose_name=u'Nr rejestru')
    
    datatype = models.IntegerField(choices=SENSOR_DATATYPE, verbose_name=u'Typ danej')
    esemantic = models.IntegerField(choices=SENSOR_ESEMANTIC, verbose_name=u'Semantyka błędów')
    
    interval_0 = models.IntegerField(verbose_name=u'Interwał runlevel 0')
    interval_1 = models.IntegerField(verbose_name=u'Interwał runlevel 1')
    
    canAdminWrite = models.BooleanField(verbose_name=u'Zmienialne?')
    canUserRead = models.BooleanField(verbose_name=u'Użytkownik może czytać')
    canUserWrite = models.BooleanField(verbose_name=u'Użytkownik może zmieniać')
    
    sorting = models.IntegerField(verbose_name=u'Nr sortowania')

    def fromStorage(self, value):
        '''dostajemy z rejestru na wyswietlalna'''
        if self.datatype == 1:
            return value/10
        elif self.datatype == 2:
            v = value
            if v < 0:
                v = abs(v) + 32768
            else:
                return v/10
            v = -negate(v)
            return v/10
        else:
            return int(value)
    
    def fromUserinput(self, value):
        if self.datatype == 1:
            return int(value*10)
        elif self.datatype == 2:
            value = int(value*10)
            if value < 0:
                value = negate(abs(value))
                from afruntime.numeric import uinttoint
                return uinttoint(value)
            else:
                return int(value)
        else:
            return int(value)
    
    def getLastRead(self):
        import patelnia.p24
        from patelnia.p24.Exceptions import NotReaded, ReadErrored
        s = patelnia.p24.Sensor(patelnia.p24.Device(self.Device.dev_number), self.modbus_devid, self.regtype, self.register)
        try:
            res = int(s)
            ttime = s.getReadTime()
        except NotReaded:
            res = 'NOTREADED'
            ttime = None
        except ReadErrored:
            res = 'ERROR'
            ttime = None
        else:
            if ((res < -300) or (res > 1500)) and (self.esemantic == 1) and (self.datatype == 1):
                return ('AWARIA',ttime)
            if self.datatype == 1:
                res = res / 10
            if self.datatype == 2:
                res = self.fromStorage(res)
                    
        return (res,ttime)
    
    def lsRepr(self):
        from patelnia.p24 import reg_typeItS
        
        return str(int(self.modbus_devid)) + reg_typeItS[self.regtype] + str(int(self.register))
    
class SensorForm(forms.ModelForm):
    class Meta:
        model = Sensor
        exclude = ('Device', )
        
    def __init__(self, *args, **kwargs):
        super(SensorForm, self).__init__(*args, **kwargs)
        for k, v in self.fields.iteritems():
            self.fields[k].error_messages = {'required':u'Pole wymagane',
                                             'invalid':u'Niepoprawny format'}

def getAfterCoords(devid, modbus_devid, reg_type, register):
    return Sensor.objects.get(modbus_devid=modbus_devid, regtype=reg_type, register=register, Device__dev_number=devid)
def getAfterPatelniaSensor(PatelniaSensor):
    return getGivenSensor(PatelniaSensor.devid, PatelniaSensor.modbus_nr, PatelniaSensor.regtype, PatelniaSensor.register)    