from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('usb_api.views',
    url(r'^$', 'home', name='home'),    
    url(r'^exchange_keys', 'exchange_keys', name='exchange_keys'),
    url(r'^transfer_shared_key', 'transfer_shared_key', name='transfer_shared_key'),
    url(r'^secure_connection', 'secure_connection', name='secure_connection'),
    url(r'^login', 'login', name='login'),
    url(r'^logout', 'logout', name='logout'),
)
