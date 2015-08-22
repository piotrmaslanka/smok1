from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('p24ip.manage',
    (r'^pick/(?P<accountdevice_id>\d+)/', 'pick.process_select'),
    (r'^pick/$', 'pick.process_list'),
    (r'^registry/$', 'registry.process'),
)
