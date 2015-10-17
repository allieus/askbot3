"""
:synopsis: django view functions for the askbot project
"""
from askbot.views import api_v1  # noqa
from askbot.views import commands  # noqa
from askbot.views import emails  # noqa
from askbot.views import meta  # noqa
from askbot.views import moderation  # noqa
from askbot.views import readers  # noqa
from askbot.views import users  # noqa
from askbot.views import widgets  # noqa
from askbot.views import writers  # noqa
from django.conf import settings as django_settings

if 'avatar' in django_settings.INSTALLED_APPS:
    from askbot.views import avatar_views  # noqa
