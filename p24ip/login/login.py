from djangomako.shortcuts import render_to_response
from p24ip.login.models import LoginForm, Account
from django.shortcuts import redirect
from django.views.decorators.cache import cache_page

def process(request):
    if request.method == 'POST':
        lf = LoginForm(request.POST)
        if lf.is_valid():
            acc = Account.objects.get(login=lf.cleaned_data['login'])
            request.session['logged'] = True
            request.session['Account.id'] = acc.id
            request.session['Account.privileges'] = acc.privileges
            request.session['device_picked'] = False
            return redirect('/manage/pick/')
    try:
        lf
    except:
        lf = LoginForm()        
    
    return render_to_response('login/login.html', {'form':lf,'request':request})    


process = cache_page(process, 60 * 60 * 24 * 7)