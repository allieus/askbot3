# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import keyedcache.models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LongSetting',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('group', models.CharField(max_length=100)),
                ('key', models.CharField(max_length=100)),
                ('value', models.TextField(blank=True)),
                ('site', models.ForeignKey(verbose_name='Site', to='sites.Site')),
            ],
            options={
                'db_table': 'livesettings_longsetting',
            },
            bases=(models.Model, keyedcache.models.CachedObjectMixin),
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('group', models.CharField(max_length=100)),
                ('key', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=255, blank=True)),
                ('site', models.ForeignKey(verbose_name='Site', to='sites.Site')),
            ],
            options={
                'db_table': 'livesettings_setting',
            },
            bases=(models.Model, keyedcache.models.CachedObjectMixin),
        ),
        migrations.AlterUniqueTogether(
            name='setting',
            unique_together=set([('site', 'group', 'key')]),
        ),
        migrations.AlterUniqueTogether(
            name='longsetting',
            unique_together=set([('site', 'group', 'key')]),
        ),
    ]
