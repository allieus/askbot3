# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0011_auto_20151021_1610'),
    ]

    operations = [
        migrations.CreateModel(
            name='LastVisitTime',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'group_messaging_lastvisittime',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('message_type', models.SmallIntegerField(default=0, choices=[(0, 'email-like message, stored in the inbox'), (2, 'will be shown just once'), (1, 'will be shown until certain time')])),
                ('senders_info', models.TextField(default='')),
                ('headline', models.CharField(max_length=80)),
                ('text', models.TextField(help_text='source text for the message, e.g. in markdown format', null=True, blank=True)),
                ('html', models.TextField(help_text='rendered html of the message', null=True, blank=True)),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('last_active_at', models.DateTimeField(auto_now_add=True)),
                ('active_until', models.DateTimeField(null=True, blank=True)),
                ('parent', models.ForeignKey(related_name='children', to='group_messaging.Message', null=True, blank=True)),
                ('recipients', models.ManyToManyField(to='auth.Group')),
                ('root', models.ForeignKey(related_name='descendants', to='group_messaging.Message', null=True, blank=True)),
                ('sender', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='group_messaging_sent_messages')),
            ],
            options={
                'db_table': 'group_messaging_message',
            },
        ),
        migrations.CreateModel(
            name='MessageMemo',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('status', models.SmallIntegerField(default=0, choices=[(0, 'seen'), (1, 'archived'), (2, 'deleted')])),
                ('message', models.ForeignKey(to='group_messaging.Message', related_name='memos')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'group_messaging_messagememo',
            },
        ),
        migrations.CreateModel(
            name='SenderList',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('recipient', models.OneToOneField(to='auth.Group')),
                ('senders', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'group_messaging_senderlist',
            },
        ),
        migrations.CreateModel(
            name='UnreadInboxCounter',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('count', models.PositiveIntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'group_messaging_unreadinboxcounter',
            },
        ),
        migrations.AddField(
            model_name='lastvisittime',
            name='message',
            field=models.ForeignKey(to='group_messaging.Message'),
        ),
        migrations.AddField(
            model_name='lastvisittime',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='messagememo',
            unique_together=set([('user', 'message')]),
        ),
        migrations.AlterUniqueTogether(
            name='lastvisittime',
            unique_together=set([('user', 'message')]),
        ),
    ]
