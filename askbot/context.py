"""Askbot template context processor that makes some parameters
from the django settings, all parameters from the askbot livesettings
and the application available for the templates"""

import sys
import json
from django.conf import settings as django_settings
from django.core.urlresolvers import reverse
import askbot
from askbot import api
from askbot import models
from askbot import const
from askbot.conf import settings as askbot_settings
from askbot.search.state_manager import SearchState
from askbot.utils import url_utils
from askbot.utils.csrf import get_or_create_csrf_token
from askbot.utils.slug import slugify
from askbot.utils.html import site_url
from askbot.utils.translation import get_language


def application_settings(request):
    """The context processor function"""
    # if not request.path.startswith('/' + settings.ASKBOT_URL):
    #    # TODO: this is a really ugly hack, will only work
    #    # when askbot is installed not at the home page.
    #    # this will not work for the
    #    # heavy modders of askbot, because their custom pages
    #    # will not receive the askbot settings in the context
    #    # to solve this properly we should probably explicitly
    #    # add settings to the context per page
    #    return {}
    my_settings = askbot_settings.as_dict()

    my_settings.update({
        'USE_ASKBOT_LOGIN_SYSTEM': False,  # FIXME: not using django_authopenid
        'LANGUAGE_CODE': getattr(request, 'LANGUAGE_CODE', django_settings.LANGUAGE_CODE),
        'MULTILINGUAL': False,  # FIXME: REMOVE ME
        'LANGUAGES_DICT': dict(getattr(django_settings, 'LANGUAGES', [])),
        'ALLOWED_UPLOAD_FILE_TYPES': django_settings.ASKBOT_ALLOWED_UPLOAD_FILE_TYPES,
        'ASKBOT_URL': django_settings.ASKBOT_URL,
        'STATIC_URL': django_settings.STATIC_URL,
        'IP_MODERATION_ENABLED': getattr(django_settings, 'ASKBOT_IP_MODERATION_ENABLED', False),
        'USE_LOCAL_FONTS': getattr(django_settings, 'ASKBOT_USE_LOCAL_FONTS', False),
        'CSRF_COOKIE_NAME': django_settings.CSRF_COOKIE_NAME,
        'DEBUG': django_settings.DEBUG,
        'USING_RUNSERVER': 'runserver' in sys.argv or 'runserver_plus' in sys.argv,
        'ASKBOT_VERSION': askbot.get_version(),
        'LOGIN_URL': url_utils.get_login_url(),
        'LOGOUT_URL': url_utils.get_logout_url(),
        'LOGOUT_REDIRECT_URL': url_utils.get_logout_redirect_url(),
        'TINYMCE_PLUGINS': [],
    })

    if my_settings['EDITOR_TYPE'] == 'tinymce':
        tinymce_plugins = django_settings.TINYMCE_DEFAULT_CONFIG.get('plugins', '').split(',')
        my_settings['TINYMCE_PLUGINS'] = list(map(lambda v: v.strip(), tinymce_plugins))

    current_language = get_language()

    # for some languages we will start searching for shorter words
    if current_language == 'ja':
        # we need to open the search box and show info message about the japanese lang search
        min_search_word_length = 1
    else:
        min_search_word_length = my_settings['MIN_SEARCH_WORD_LENGTH']

    need_scope_links = askbot_settings.ALL_SCOPE_ENABLED or \
        askbot_settings.UNANSWERED_SCOPE_ENABLED or \
        (request.user.is_authenticated() and askbot_settings.FOLLOWED_SCOPE_ENABLED)

    context = {
        'base_url': site_url(''),
        'csrf_token': get_or_create_csrf_token(request),
        'empty_search_state': SearchState.get_empty(),
        'min_search_word_length': min_search_word_length,
        'current_language_code': current_language,
        'settings': my_settings,
        'need_scope_links': need_scope_links,
        'noscript_url': const.DEPENDENCY_URLS['noscript'],
    }

    if hasattr(request, 'user'):
        context['moderation_items'] = api.get_info_on_moderation_items(request.user)

    group_list = list()

    if askbot_settings.GROUPS_ENABLED:
        # calculate context needed to list all the groups
        def _get_group_url(group):
            """calculates url to the group based on its id and name"""
            group_slug = slugify(group['name'])
            return reverse(
                'users_by_group',
                kwargs={'group_id': group['id'], 'group_slug': group_slug}
            )

        # load id's and names of all groups
        global_group = models.Group.objects.get_global_group()
        groups = models.Group.objects.exclude_personal()
        groups = groups.exclude(id=global_group.id)
        groups_data = list(groups.values('id', 'name'))

        # sort groups_data alphanumerically, but case-insensitive
        groups_data = sorted(groups_data, key=lambda data: data['name'].lower())

        # insert data for the global group at the first position
        groups_data.insert(0, {'id': global_group.id, 'name': global_group.name})

        for group in groups_data:
            link = _get_group_url(group)
            group_list.append({'name': group['name'], 'link': link})

    context['group_list'] = json.dumps(group_list)

    return context

