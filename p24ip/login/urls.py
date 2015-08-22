from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('p24ip.login',
    (r'^login/', 'login.process'),
    (r'^logout/', 'logout.process'),
)
