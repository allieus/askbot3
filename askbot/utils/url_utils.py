from django.core.urlresolvers import reverse
from django.conf import settings
from django.conf.urls import url
from django.utils import translation
from django.utils.six.moves.urllib.parse import urlparse, urlunparse, ParseResult


def reverse_i18n(lang, *args, **kwargs):
    """reverses url in requested language"""
    assert(lang is not None)
    current_lang = translation.get_language()
    translation.activate(lang)
    url = reverse(*args, **kwargs)
    translation.activate(current_lang)
    return url


def service_url(*args, **kwargs):
    """adds the service prefix to the url"""
    pattern = args[0]
    if pattern[0] == '^':
        pattern = pattern[1:]

    prefix = getattr(settings, 'ASKBOT_SERVICE_URL_PREFIX', '')
    pattern = '^' + prefix + pattern
    new_args = list(args)
    new_args[0] = pattern
    return url(*new_args, **kwargs)


def strip_path(url):
    """srips path, params and hash fragments of the url"""
    purl = urlparse(url)
    return urlunparse(
        ParseResult(
            purl.scheme,
            purl.netloc,
            '', '', '', ''
        )
    )


def append_trailing_slash(urlpath):
    """if path is empty - returns slash
    if not and path does not end with the slash
    appends it
    """
    if urlpath == '':
        return '/'
    elif not urlpath.endswith('/'):
        return urlpath + '/'
    return urlpath


def urls_equal(url1, url2, ignore_trailing_slash=False):
    """True, if urls are equal"""
    purl1 = urlparse(url1)
    purl2 = urlparse(url2)
    if purl1.scheme != purl2.scheme:
        return False

    if purl1.netloc != purl2.netloc:
        return False

    if ignore_trailing_slash is True:
        normfunc = append_trailing_slash
    else:
        normfunc = lambda v: v

    if normfunc(purl1.path) != normfunc(purl2.path):
        return False

    # test remaining items in the parsed url
    return purl1[3:] == purl2[3:]


def get_login_url():
    return settings.LOGIN_URL


def get_logout_url():
    return settings.LOGOUT_URL


def get_logout_redirect_url():
    if hasattr(settings, 'LOGOUT_REDIRECT_URL'):
        return settings.LOGOUT_REDIRECT_URL
    else:
        return reverse('index')

