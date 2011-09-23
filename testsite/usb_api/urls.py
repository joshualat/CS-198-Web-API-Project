from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('usb_api.views',
    url(r'^$', 'home', name='home'),    
    url(r'^test', 'test', name='test'),
)
