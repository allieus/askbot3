import traceback
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.utils import six
from livesettings import ConfigurationSettings, forms
from livesettings import ImageValue
from livesettings.overrides import get_overrides
from askbot.utils.decorators import admins_only
import logging

log = logging.getLogger('configuration.views')


@never_cache
@admins_only
def group_settings(request, group, template='livesettings/group_settings.jinja'):
    # Determine what set of settings this editor is used for

    use_db, overrides = get_overrides()

    mgr = ConfigurationSettings()

    settings = mgr[group]
    title = settings.name
    log.debug('title: %s', title)

    if use_db:
        # Create an editor customized for the current user
        # editor = forms.customized_editor(settings)
        if request.method == 'POST':
            # Populate the form with user-submitted data
            data = request.POST.copy()
            form = forms.SettingsEditor(data, request.FILES, settings=settings)
            if form.is_valid():
                for name, value in form.cleaned_data.items():
                    group, key, lang = name.split('__')
                    cfg = mgr.get_config(group, key)

                    if isinstance(cfg, ImageValue):
                        if request.FILES and name in request.FILES:
                            value = request.FILES[name]
                        else:
                            continue

                    try:
                        cfg.update(value, lang)
                        # message='Updated %s on %s' % (cfg.key, cfg.group.key)
                        # messages.success(request, message)
                        # the else if for the settings that are not updated.
                    except Exception as e:
                        traceback.print_exc()
                        request.user.message_set.create(message=six.text_type(e))

                return redirect(request.path)
        else:
            # Leave the form populated with current setting values
            # form = editor()
            form = forms.SettingsEditor(settings=settings)
    else:
        form = None

    return render(request, template, {
        'all_super_groups': mgr.get_super_groups(),
        'title': title,
        'settings_group': settings,
        'form': form,
        'use_db': use_db
    })


# Site-wide setting editor is identical, but without a group
# staff_member_required is implied, since it calls group_settings
def site_settings(request):
    mgr = ConfigurationSettings()
    default_group = mgr.groups()[0].key
    return redirect('group_settings', default_group)
    # return group_settings(request, group=None, template='livesettings/site_settings.jinja')


@never_cache
@admins_only
def export_as_python(request):
    """Export site settings as a dictionary of dictionaries"""

    from livesettings.models import Setting, LongSetting
    import pprint

    work = {}
    both = list(Setting.objects.all())
    both.extend(list(LongSetting.objects.all()))

    for s in both:
        if s.site.id not in work:
            work[s.site.id] = {}
        sitesettings = work[s.site.id]

        if s.group not in sitesettings:
            sitesettings[s.group] = {}
        sitegroup = sitesettings[s.group]

        sitegroup[s.key] = s.value

    pp = pprint.PrettyPrinter(indent=4)
    pretty = pp.pformat(work)

    return render(request, 'livesettings/text.txt.jinja', {
        'text': pretty,
    }, content_type='text/plain')

