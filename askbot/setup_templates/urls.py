"""
main url configuration file for the askbot site
"""
from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
from askbot.views.error import internal_error as handler500

admin.autodiscover()

urlpatterns = [
    url(r'%s' % settings.ASKBOT_URL, include('askbot.urls'))
]

urlpatterns += [
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^cache/', include('keyedcache.urls')), - broken views disable for now
    # url(r'^settings/', include('livesettings.urls')),
    url(r'^followit/', include('followit.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^robots.txt$', include('robots.urls')),
    url(  # TODO: replace with django.conf.urls.static ?
        r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:],
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT.replace('\\', '/')},
    ),
]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',  # noqa
        url(r'^rosetta/', include('rosetta.urls')),
    )

handler500 = 'askbot.views.error.internal_error'  # noqa

