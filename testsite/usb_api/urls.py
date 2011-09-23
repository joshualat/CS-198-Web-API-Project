from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('usb_api.views',
    url(r'^$', 'home', name='home'),    
    url(r'^exchange_keys', 'exchange_keys', name='exchange_keys'),
    url(r'^test', 'test', name='test'),
)
