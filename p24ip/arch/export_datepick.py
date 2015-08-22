# coding=UTF-8
from p24ip.login.decorators import must_be_logged, must_pick_device, must_be_service
from djangomako.shortcuts import render_to_response
from p24ip.arch.models import Read
from django.shortcuts import redirect
from django import forms
from p24ip.manage import get_struct

DATEPICK_PRESENTATION = ((0, 'Excel'), 
                         (1, 'Ekstrema'),
                        )

class DatepickForm(forms.Form):
    dfrom = forms.DateField(label=u'Od', help_text=u'Rok-miesiąc-dzień')
    dto = forms.DateField(label=u'Do', help_text=u'Rok-miesiąc-dzień')
    method = forms.ChoiceField(choices=DATEPICK_PRESENTATION, label=u'Format')


@must_be_logged
@must_pick_device
@must_be_service
def process(request):
    struct = get_struct(request).exports
    if request.method == 'POST':
        rf = DatepickForm(request.POST)
        rf.fields['method'].choices = struct.EXPORTS(DATEPICK_PRESENTATION)
        if rf.is_valid():
            s = int(rf.cleaned_data['method'])
            if s == 0:
                from p24ip.arch.sopmods import excel
                return excel.process(request, rf.cleaned_data['dfrom'], rf.cleaned_data['dto'])
            if s == 1:
                from p24ip.arch.sopmods import extrema
                return extrema.process(request, rf.cleaned_data['dfrom'], rf.cleaned_data['dto'])
            else:
                return struct.__dict__['export'+str(s)](request, rf.cleaned_data['dfrom'], rf.cleaned_data['dto'])
            
    else:
        rf = DatepickForm()
        rf.fields['method'].choices = struct.EXPORTS(DATEPICK_PRESENTATION)
    return render_to_response('arch/export_datepick.html', {'request':request, 'form':rf})

