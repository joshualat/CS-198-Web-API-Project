from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^usb/', include('testsite.usb_api.urls')),
    url(r'^', include('testsite.core.urls')),
)

# Serving of static media using Django is enabled only when
# settings.USE_STATIC = True
from django.conf import settings
if getattr(settings, 'USE_STATIC', True):
    urlpatterns += patterns('',
        (r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:],
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT })
    )
