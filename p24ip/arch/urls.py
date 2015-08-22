from django.conf.urls.defaults import *

urlpatterns = patterns('p24ip.arch',
    (r'^setup/make/(?P<sensor_id>\d+)/', 'setup.makeArch'),
    (r'^setup/unmake/(?P<sensor_id>\d+)/', 'setup.unmakeArch'),
    (r'^setup/save/', 'setup.storeArchSettings'),
    
    
    (r'^export/datepick/', 'export_datepick.process'),
)
