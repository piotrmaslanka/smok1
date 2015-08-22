# coding=UTF-8
from django.db import models
from django import forms
from p24ip.login.models import Account

ACCOUNTDEVICE_PRIVILEGES = ((0, 'Użytkownik'),
                            (1, 'Serwis'))

class BigIntegerField(models.IntegerField):
    empty_strings_allowed = False
    def get_internal_type(self):
        return "BigIntegerField"
    def db_type(self):
        return 'bigint'

class Device(models.Model):
    dev_number = BigIntegerField(verbose_name=u'ID')
    short_name = models.CharField(max_length=40, verbose_name=u'Nazwa')
    description = models.TextField(verbose_name=u'Opis')
    localisation = models.CharField(max_length=80, verbose_name=u'Lokalizacja')
    
    def isOnline(self):
        from patelnia.p24 import Device
        d = Device(self.dev_number)
        return d.isOnline()
    
    def isAlert(self):
        from patelnia.p24 import Device
        try:
            return Device(self.dev_number).registry['alert'] == '1'
        except:
            return False

class AccountDevice(models.Model):
    Account = models.ForeignKey(Account)
    Device = models.ForeignKey(Device)
    privileges = models.IntegerField(choices=ACCOUNTDEVICE_PRIVILEGES, verbose_name=u'Uprawnienia')

