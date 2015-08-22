from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^login/', include('p24ip.login.urls')),
    (r'^manage/', include('p24ip.manage.urls')),
    (r'^device/', include('p24ip.device.urls')),
    (r'^arch/', include('p24ip.arch.urls')),
    (r'^dispatch/', include('p24ip.dispatch.urls')),
    (r'^$', 'p24ip.publica.static.index'),
    (r'^sitemap.xml', 'p24ip.publica.static.sitemap'),
    (r'^about/', 'p24ip.publica.static.about'),
)
