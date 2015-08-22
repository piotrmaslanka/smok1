from django.shortcuts import redirect
from django.http import HttpResponse

def must_be_logged(process):
    def must_be_logged_decorator(*args, **kwargs):
        try:
            if not (args[0].session['logged']):
                return redirect('/login/login/')
            return process(*args, **kwargs)
        except:
            return process(*args, **kwargs)
    return must_be_logged_decorator

def must_be_logged_ajax(process):
    def must_be_logged_decorator(*args, **kwargs):
        try:
            if not (args[0].session['logged']):
                return HttpResponse('NOT_LOGGED')
            return process(*args, **kwargs)
        except:
            return process(*args, **kwargs)
    return must_be_logged_decorator

def must_pick_device(process):
    def must_pick_device_decorator(*args, **kwargs):
        try:
            if not (args[0].session['device_picked']):
                return redirect('/manage/pick/')
            return process(*args, **kwargs)
        except:
            return process(*args, **kwargs)
    return must_pick_device_decorator

def must_pick_device_ajax(process):
    def must_pick_device_decorator(*args, **kwargs):
        try:
            if not (args[0].session['device_picked']):
                return HttpResponse('PICK_DEVICE')
            return process(*args, **kwargs)
        except:
            return process(*args, **kwargs)
    return must_pick_device_decorator

def must_be_service(process):
    def must_be_service_decorator(*args, **kwargs):
        try:
            if not (args[0].session['AccountDevice.privileges']==1):
                return redirect('/manage/pick')
            return process(*args, **kwargs)
        except:
            return process(*args, **kwargs)
    return must_be_service_decorator
def must_be_service_ajax(process):
    def must_be_service_decorator(*args, **kwargs):
        try:
            if not (args[0].session['AccountDevice.privileges']==1):
                return HttpResponse('MUST_BE_SERVICE')
            return process(*args, **kwargs)
        except:
            return process(*args, **kwargs)
    return must_be_service_decorator

def must_be_admin(process):
    def must_be_admin_decorator(*args, **kwargs):
        try:
            if args[0].session['Account.privileges'] != 1:
                return redirect('/login/login/')
            return process(*args, **kwargs)
        except:
            return process(*args, **kwargs)
    return must_be_admin_decorator
