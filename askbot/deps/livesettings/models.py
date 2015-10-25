from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy
from keyedcache import cache_key as cache_key_get, cache_get, cache_set, NotCachedError
from keyedcache.models import CachedObjectMixin
from livesettings.compat import get_cache_timeout
from livesettings.overrides import get_overrides
import logging

logger = logging.getLogger('configuration.models')

__all__ = ['SettingNotSet', 'Setting', 'LongSetting', 'find_setting']


def _safe_get_site_id(site):
    if not site:
        try:
            site = Site.objects.get_current()
            site_id = site.id
        except:
            site_id = settings.SITE_ID
    else:
        site_id = site.id
    return site_id


def find_setting(group, key, site=None):
    'Get a setting or longsetting by group and key, cache and return it.'

    site_id = _safe_get_site_id(site)
    setting = None

    use_db, overrides = get_overrides(site_id)
    ck = cache_key_get('Setting', site_id, group, key)

    grp = overrides.get(group, None)

    if grp and (key in grp):
        val = grp[key]
        setting = ImmutableSetting(key=key, group=group, value=val)
        logger.debug('Returning overridden: %s', setting)

    elif use_db:
        try:
            setting = cache_get(ck)
        except NotCachedError:
            model_classes = (Setting, LongSetting)
            for model_cls in model_classes:
                try:
                    setting = model_cls.objects.get(site__id=site_id, key=key, group=group)
                    break
                except model_cls.DoesNotExist:
                    pass

            cache_set(ck, value=setting)
    else:
        grp = overrides.get(group, None)
        if grp and key in grp:
            val = grp[key]
            setting = ImmutableSetting(key=key, group=group, value=val)
            logger.debug('Returning overridden: %s', setting)

    if setting is None:
        raise SettingNotSet(key, cachekey=ck)

    return setting


class SettingNotSet(Exception):
    def __init__(self, k, cachekey=None):
        self.key = k
        self.cachekey = cachekey
        self.args = [self.key, self.cachekey]


class SettingManager(models.Manager):
    def get_queryset(self):
        all = super(SettingManager, self).get_queryset()
        site_id = _safe_get_site_id(None)
        return all.filter(site__id=site_id)


class ImmutableSetting(object):
    def __init__(self, group='', key='', value='', site=1):
        self.site = site
        self.group = group
        self.key = key
        self.value = value

    def cache_key(self, *args, **kwargs):
        return cache_key_get('OverrideSetting', self.site, self.group, self.key)

    def delete(self):
        pass

    def save(self, *args, **kwargs):
        pass

    def __repr__(self):
        return 'ImmutableSetting: %s.%s=%s' % (self.group, self.key, self.value)


class Setting(models.Model, CachedObjectMixin):
    site = models.ForeignKey(Site, verbose_name=ugettext_lazy('Site'))
    group = models.CharField(max_length=100, blank=False, null=False)
    key = models.CharField(max_length=100, blank=False, null=False)
    value = models.CharField(max_length=255, blank=True)

    objects = SettingManager()

    class Meta:
        app_label = 'livesettings'
        db_table = 'livesettings_setting'
        unique_together = ('site', 'group', 'key')

    def __nonzero__(self):
        return self.id is not None

    def cache_key(self, *args, **kwargs):
        return cache_key_get('Setting', self.site, self.group, self.key)

    def delete(self):
        self.cache_delete()
        super(Setting, self).delete()

    def save(self, force_insert=False, force_update=False):
        try:
            site = self.site
        except Site.DoesNotExist:
            self.site = Site.objects.get_current()

        super(Setting, self).save(force_insert=force_insert, force_update=force_update)

        self.cache_set()

    def cache_set(self, *args, **kwargs):
        val = kwargs.pop('value', self)
        key = self.cache_key(*args, **kwargs)
        length = get_cache_timeout()
        cache_set(key, value=val, length=length)


class LongSettingManager(models.Manager):
    def get_queryset(self):
        all = super(LongSettingManager, self).get_queryset()
        site_id = _safe_get_site_id(None)
        return all.filter(site__id=site_id)


class LongSetting(models.Model, CachedObjectMixin):
    'A Setting which can handle more than 255 characters'
    site = models.ForeignKey(Site, verbose_name=ugettext_lazy('Site'))
    group = models.CharField(max_length=100, blank=False, null=False)
    key = models.CharField(max_length=100, blank=False, null=False)
    value = models.TextField(blank=True)

    objects = LongSettingManager()

    class Meta:
        app_label = 'livesettings'
        db_table = 'livesettings_longsetting'
        unique_together = ('site', 'group', 'key')

    def __nonzero__(self):
        return self.id is not None

    def cache_key(self, *args, **kwargs):
        # note same cache pattern as Setting.  This is so we can look up in one check.
        # they can't overlap anyway, so this is moderately safe.  At the worst, the
        # Setting will override a LongSetting.
        return cache_key_get('Setting', self.site, self.group, self.key)

    def delete(self):
        self.cache_delete()
        super(LongSetting, self).delete()

    def save(self, force_insert=False, force_update=False):
        try:
            site = self.site
        except Site.DoesNotExist:
            self.site = Site.objects.get_current()
        super(LongSetting, self).save(force_insert=force_insert, force_update=force_update)
        self.cache_set()

    def cache_set(self, *args, **kwargs):
        val = kwargs.pop('value', self)
        key = self.cache_key(*args, **kwargs)
        length = get_cache_timeout()
        cache_set(key, value=val, length=length)


