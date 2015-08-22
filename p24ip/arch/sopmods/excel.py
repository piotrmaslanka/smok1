# coding=UTF-8
from django.http import HttpResponse
import xlwt as Excel
from tempfile import mktemp  # Tak, wiem o wyścigach w /tmp
from p24ip.arch.models import ArchSensor    
    
def process(request, dfrom, dto):
    # Prepare reads
    
    archsensors = ArchSensor.objects.filter(Sensor__Device__id=request.session['Device.id'])
    
    doc = Excel.Workbook()
    
    datestyle = Excel.XFStyle()
    datestyle.num_format_str = 'DD/MM/YYYY hh:mm:ss'
    
    sheets = {}
    indices = {}
    
    for archsensor in archsensors:
        name = archsensor.Sensor.name
        csheet = doc.add_sheet(name)
        
        csheet.write(0,0,u'Data')
        csheet.write(0,1,u'Wartość')
        indices[name] = 1
        
        reads = archsensor.read_set.filter(readed_on__lte=dto).filter(readed_on__gte=dfrom).exclude(data=None).order_by('readed_on')
        sensor = archsensor.Sensor    
        for elem in reads:
            csheet.write(indices[name], 0, elem.readed_on, datestyle)
            csheet.write(indices[name], 1, sensor.fromStorage(elem.data))
            indices[name] = indices[name] + 1
        sheets[name] = csheet
                                
    filename = mktemp()
    doc.save(filename)
    x = open(filename,'r')
    req = HttpResponse(x.read(), mimetype='application/vnd.ms-excel')
    req['Content-Disposition'] = 'attachment; filename='+str(request.session['Device.id'])+'.xls'
    return req