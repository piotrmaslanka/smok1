# coding=UTF-8
from __future__ import division
from p24ip.manage.models import Device
from p24ip.device.models import Sensor 
from django.db import models
from django import forms

class ArchSensor(models.Model):
    Sensor = models.ForeignKey(Sensor)
    
class Read(models.Model):
    ArchSensor = models.ForeignKey(ArchSensor)
    readed_on = models.DateTimeField()
    data = models.IntegerField(null=True)
    
    def __unicode__(self):
        return str(self.id)+' ArchSensor: '+str(self.ArchSensor.id)+' '+str(self.readed_on)+' '+str(self.data)