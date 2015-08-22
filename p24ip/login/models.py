# coding=UTF-8
from django.db import models
from django import forms

ACCOUNT_PRIVILEGES = ((0, 'Użytkownik'),
                      (1, 'Serwis'))

class Account(models.Model):
    login = models.CharField(max_length=20, verbose_name=u'Login')
    password = models.CharField(max_length=40, verbose_name=u'SHA-1 hasła')
    name = models.CharField(max_length=30, verbose_name=u'Nazwa')
    address = models.CharField(max_length=50, verbose_name=u'Adres')
    postal = models.CharField(max_length=30, verbose_name=u'Kod, miasto')
    phone = models.CharField(max_length=30, verbose_name=u'Telefon')
    privileges = models.PositiveSmallIntegerField(choices=ACCOUNT_PRIVILEGES, default=0)
    
class LoginForm(forms.Form):
    '''Form used in logon script'''
    login = forms.CharField(label='Login', max_length=20)
    password = forms.CharField(label='Hasło', max_length=40, widget=forms.PasswordInput)
    
    def clean(self):
        '''Checks whether the login and password are valid'''
        from hashlib import sha1
        
        try:
            acc, = Account.objects.filter(login=self.cleaned_data['login']).filter(password=sha1(self.cleaned_data['password']).hexdigest())
        except ValueError:
            raise forms.ValidationError('Dane niepoprawne')
        except KeyError:
            return self.cleaned_data
        return self.cleaned_data            