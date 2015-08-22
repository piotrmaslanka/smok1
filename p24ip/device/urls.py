from django.conf.urls.defaults import *

urlpatterns = patterns('p24ip.device',
    (r'^overview/$', 'overview.process'),
    (r'^sensors/control/$', 'control.display'),
    (r'^sensors/control/ajax/$', 'control.ajax'),
    (r'^sensors/setup/list/$', 'setup.sensors_list'),
    (r'^sensors/setup/save/$', 'setup.save'),
    (r'^sensors/setup/edit/(?P<sensor_id>\d+)/$', 'setup.sensor_edit'),
    (r'^sensors/setup/new/$', 'setup.sensor_new'),
    (r'^sensors/setup/delete/(?P<sensor_id>\d+)/$', 'setup.sensor_delete'),
    (r'^own/(?P<site_name>.*?)/$', 'own.control'),
    (r'^registry/$', 'registry.process'),
    (r'^alertlog/$', 'alertlog.process'), 
    (r'^alertlog/yellow/$', 'alertlog.yellow'), 
    (r'^alertlog/red/$', 'alertlog.red'),
    (r'^restat/clearstats/$', 'restat.clearstats'),
    (r'^restat/errtoggle/$', 'restat.errtoggle'),
)
