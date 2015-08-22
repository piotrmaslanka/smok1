from p24ip.login.decorators import must_be_logged
from django.shortcuts import redirect

@must_be_logged
def process(request):
    request.session['logged'] = False
    del request.session['Account.id']
    del request.session['Account.privileges']
    del request.session['device_picked']
    return redirect('/login/login')    
