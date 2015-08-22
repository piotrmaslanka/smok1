from p24ip.login.decorators import must_be_logged
from djangomako.shortcuts import render_to_response
from p24ip.manage.models import AccountDevice
from django.shortcuts import redirect

@must_be_logged
def process_select(request, accountdevice_id):
    try:
        ad = AccountDevice.objects.get(id=int(accountdevice_id))
        if ad.Account.id != request.session['Account.id']:
            raise Exception
    except:
        return redirect('/manage/pick/')
    
    
    request.session['Device.id'] = ad.Device.id
    request.session['Device.dev_number'] = ad.Device.dev_number
    request.session['device_picked'] = True
    request.session['AccountDevice.id'] = ad.id
    request.session['AccountDevice.short_name'] = ad.Device.short_name
    request.session['AccountDevice.privileges'] = ad.privileges
        
    return redirect('/device/overview/')
    
     

@must_be_logged
def process_list(request):
    ads = AccountDevice.objects.filter(Account=request.session['Account.id'])
    return render_to_response('manage/pick.list.html', {'ads':ads,'request':request})