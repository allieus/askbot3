# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0007_auto_20151015_1418'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LastVisitTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('message_type', models.SmallIntegerField(choices=[(0, 'email-like message, stored in the inbox'), (2, 'will be shown just once'), (1, 'will be shown until certain time')], default=0)),
                ('senders_info', models.TextField(default='')),
                ('headline', models.CharField(max_length=80)),
                ('text', models.TextField(null=True, help_text='source text for the message, e.g. in markdown format', blank=True)),
                ('html', models.TextField(null=True, help_text='rendered html of the message', blank=True)),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('last_active_at', models.DateTimeField(auto_now_add=True)),
                ('active_until', models.DateTimeField(null=True, blank=True)),
                ('parent', models.ForeignKey(null=True, blank=True, to='group_messaging.Message', related_name='children')),
                ('recipients', models.ManyToManyField(to='auth.Group')),
                ('root', models.ForeignKey(null=True, blank=True, to='group_messaging.Message', related_name='descendants')),
                ('sender', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='group_messaging_sent_messages')),
            ],
        ),
        migrations.CreateModel(
            name='MessageMemo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('status', models.SmallIntegerField(choices=[(0, 'seen'), (1, 'archived'), (2, 'deleted')], default=0)),
                ('message', models.ForeignKey(to='group_messaging.Message', related_name='memos')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SenderList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('recipient', models.ForeignKey(unique=True, to='auth.Group')),
                ('senders', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UnreadInboxCounter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('count', models.PositiveIntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
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
