# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import picklefield.fields
import keyedcache.models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0007_auto_20151015_1418'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('activity_type', models.SmallIntegerField(db_index=True, choices=[(1, 'asked a question'), (2, 'answered a question'), (3, 'commented question'), (4, 'commented answer'), (5, 'edited question'), (6, 'edited answer'), (7, 'received badge'), (8, 'marked best answer'), (9, 'upvoted'), (10, 'downvoted'), (11, 'canceled vote'), (12, 'deleted question'), (13, 'deleted answer'), (14, 'marked offensive'), (15, 'updated tags'), (16, 'selected favorite'), (17, 'completed user profile'), (18, 'email update sent to user'), (29, 'a post was shared'), (20, 'reminder about unanswered questions sent'), (21, 'reminder about accepting the best answer sent'), (19, 'mentioned in the post'), (22, 'created tag description'), (23, 'updated tag description'), (24, 'made a new post'), (25, 'made an edit'), (26, 'created post reject reason'), (27, 'updated post reject reason'), (28, 'sent email address validation message'), (31, 'sent moderation alert')])),
                ('active_at', models.DateTimeField(default=datetime.datetime.now)),
                ('object_id', models.PositiveIntegerField(db_index=True)),
                ('is_auditted', models.BooleanField(default=False)),
                ('summary', models.TextField(default='')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'db_table': 'activity',
            },
        ),
        migrations.CreateModel(
            name='ActivityAuditStatus',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('status', models.SmallIntegerField(choices=[(0, 'new'), (1, 'seen')], default=0)),
                ('activity', models.ForeignKey(to='askbot.Activity')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'askbot_activityauditstatus',
            },
        ),
        migrations.CreateModel(
            name='AnonymousAnswer',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('session_key', models.CharField(max_length=40)),
                ('wiki', models.BooleanField(default=False)),
                ('added_at', models.DateTimeField(default=datetime.datetime.now)),
                ('ip_addr', models.GenericIPAddressField()),
                ('text', models.TextField()),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AnonymousQuestion',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('session_key', models.CharField(max_length=40)),
                ('wiki', models.BooleanField(default=False)),
                ('added_at', models.DateTimeField(default=datetime.datetime.now)),
                ('ip_addr', models.GenericIPAddressField()),
                ('text', models.TextField()),
                ('title', models.CharField(max_length=300)),
                ('tagnames', models.CharField(max_length=125)),
                ('is_anonymous', models.BooleanField(default=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AskWidget',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('include_text_field', models.BooleanField(default=False)),
                ('inner_style', models.TextField(blank=True)),
                ('outer_style', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('object_id', models.PositiveIntegerField()),
                ('awarded_at', models.DateTimeField(default=datetime.datetime.now)),
                ('notified', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'award',
            },
        ),
        migrations.CreateModel(
            name='BadgeData',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('slug', models.SlugField(unique=True)),
                ('awarded_count', models.PositiveIntegerField(default=0)),
                ('display_order', models.PositiveIntegerField(default=0)),
                ('awarded_to', models.ManyToManyField(through='askbot.Award', to=settings.AUTH_USER_MODEL, related_name='badges')),
            ],
            options={
                'ordering': ('display_order', 'slug'),
            },
        ),
        migrations.CreateModel(
            name='BulkTagSubscription',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('date_added', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='DraftAnswer',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('text', models.TextField(null=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='draft_answers')),
            ],
        ),
        migrations.CreateModel(
            name='DraftQuestion',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=300, null=True)),
                ('text', models.TextField(null=True)),
                ('tagnames', models.CharField(max_length=125, null=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmailFeedSetting',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('feed_type', models.CharField(max_length=16, choices=[('q_all', 'Entire forum'), ('q_ask', 'Questions that I asked'), ('q_ans', 'Questions that I answered'), ('q_sel', 'Individually selected questions'), ('m_and_c', 'Mentions and comment responses')])),
                ('frequency', models.CharField(max_length=8, choices=[('i', 'instantly'), ('d', 'daily'), ('w', 'weekly'), ('n', 'no email')], default='n')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('reported_at', models.DateTimeField(null=True)),
                ('subscriber', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='notification_subscriptions')),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteQuestion',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('added_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'favorite_question',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('group_ptr', models.OneToOneField(primary_key=True, to='auth.Group', serialize=False, auto_created=True, parent_link=True)),
                ('logo_url', models.URLField(null=True)),
                ('moderate_email', models.BooleanField(default=True)),
                ('moderate_answers_to_enquirers', models.BooleanField(help_text='If true, answers to outsiders questions will be shown to the enquirers only when selected by the group moderators.', default=False)),
                ('openness', models.SmallIntegerField(choices=[(0, 'open'), (1, 'moderated'), (2, 'closed')], default=2)),
                ('preapproved_emails', models.TextField(default='', blank=True, null=True)),
                ('preapproved_email_domains', models.TextField(default='', blank=True, null=True)),
                ('is_vip', models.BooleanField(help_text='Check to make members of this group site moderators', default=False)),
                ('read_only', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'askbot_group',
            },
            bases=('auth.group',),
        ),
        migrations.CreateModel(
            name='GroupMembership',
            fields=[
                ('authusergroups_ptr', models.OneToOneField(primary_key=True, to='auth.AuthUserGroups', serialize=False, auto_created=True, parent_link=True)),
                ('level', models.SmallIntegerField(choices=[(0, 'pending'), (1, 'full')], default=1)),
            ],
            bases=('auth.authusergroups',),
        ),
        migrations.CreateModel(
            name='ImportedObjectInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('old_id', models.IntegerField(help_text='Old object id in the source database')),
                ('new_id', models.IntegerField(help_text='New object id in the current database')),
                ('model', models.CharField(max_length=255, help_text='dotted python path to model', default='')),
                ('extra_info', picklefield.fields.PickledObjectField(editable=False, help_text='to hold dictionary for various data')),
            ],
        ),
        migrations.CreateModel(
            name='ImportRun',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('command', models.TextField(default='')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='LongSetting',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('group', models.CharField(max_length=100)),
                ('key', models.CharField(max_length=100)),
                ('value', models.TextField(blank=True)),
                ('site', models.ForeignKey(verbose_name='Site', to='sites.Site')),
            ],
            bases=(models.Model, keyedcache.models.CachedObjectMixin),
        ),
        migrations.CreateModel(
            name='MarkedTag',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('reason', models.CharField(max_length=16, choices=[('good', 'interesting'), ('bad', 'ignored'), ('subscribed', 'subscribed')])),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('post_type', models.CharField(max_length=255, db_index=True)),
                ('old_question_id', models.PositiveIntegerField(unique=True, default=None, blank=True, null=True)),
                ('old_answer_id', models.PositiveIntegerField(unique=True, default=None, blank=True, null=True)),
                ('old_comment_id', models.PositiveIntegerField(unique=True, default=None, blank=True, null=True)),
                ('added_at', models.DateTimeField(default=datetime.datetime.now)),
                ('endorsed', models.BooleanField(db_index=True, default=False)),
                ('endorsed_at', models.DateTimeField(blank=True, null=True)),
                ('approved', models.BooleanField(db_index=True, default=True)),
                ('deleted', models.BooleanField(db_index=True, default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('wiki', models.BooleanField(default=False)),
                ('wikified_at', models.DateTimeField(blank=True, null=True)),
                ('locked', models.BooleanField(default=False)),
                ('locked_at', models.DateTimeField(blank=True, null=True)),
                ('points', models.IntegerField(db_column='score', default=0)),
                ('vote_up_count', models.IntegerField(default=0)),
                ('vote_down_count', models.IntegerField(default=0)),
                ('comment_count', models.PositiveIntegerField(default=0)),
                ('offensive_flag_count', models.SmallIntegerField(default=0)),
                ('last_edited_at', models.DateTimeField(blank=True, null=True)),
                ('html', models.TextField(null=True)),
                ('text', models.TextField(null=True)),
                ('language_code', models.CharField(max_length=16, choices=[('af', 'Afrikaans'), ('ar', 'Arabic'), ('ast', 'Asturian'), ('az', 'Azerbaijani'), ('bg', 'Bulgarian'), ('be', 'Belarusian'), ('bn', 'Bengali'), ('br', 'Breton'), ('bs', 'Bosnian'), ('ca', 'Catalan'), ('cs', 'Czech'), ('cy', 'Welsh'), ('da', 'Danish'), ('de', 'German'), ('el', 'Greek'), ('en', 'English'), ('en-au', 'Australian English'), ('en-gb', 'British English'), ('eo', 'Esperanto'), ('es', 'Spanish'), ('es-ar', 'Argentinian Spanish'), ('es-mx', 'Mexican Spanish'), ('es-ni', 'Nicaraguan Spanish'), ('es-ve', 'Venezuelan Spanish'), ('et', 'Estonian'), ('eu', 'Basque'), ('fa', 'Persian'), ('fi', 'Finnish'), ('fr', 'French'), ('fy', 'Frisian'), ('ga', 'Irish'), ('gl', 'Galician'), ('he', 'Hebrew'), ('hi', 'Hindi'), ('hr', 'Croatian'), ('hu', 'Hungarian'), ('ia', 'Interlingua'), ('id', 'Indonesian'), ('io', 'Ido'), ('is', 'Icelandic'), ('it', 'Italian'), ('ja', 'Japanese'), ('ka', 'Georgian'), ('kk', 'Kazakh'), ('km', 'Khmer'), ('kn', 'Kannada'), ('ko', 'Korean'), ('lb', 'Luxembourgish'), ('lt', 'Lithuanian'), ('lv', 'Latvian'), ('mk', 'Macedonian'), ('ml', 'Malayalam'), ('mn', 'Mongolian'), ('mr', 'Marathi'), ('my', 'Burmese'), ('nb', 'Norwegian Bokmal'), ('ne', 'Nepali'), ('nl', 'Dutch'), ('nn', 'Norwegian Nynorsk'), ('os', 'Ossetic'), ('pa', 'Punjabi'), ('pl', 'Polish'), ('pt', 'Portuguese'), ('pt-br', 'Brazilian Portuguese'), ('ro', 'Romanian'), ('ru', 'Russian'), ('sk', 'Slovak'), ('sl', 'Slovenian'), ('sq', 'Albanian'), ('sr', 'Serbian'), ('sr-latn', 'Serbian Latin'), ('sv', 'Swedish'), ('sw', 'Swahili'), ('ta', 'Tamil'), ('te', 'Telugu'), ('th', 'Thai'), ('tr', 'Turkish'), ('tt', 'Tatar'), ('udm', 'Udmurt'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('vi', 'Vietnamese'), ('zh-cn', 'Simplified Chinese'), ('zh-hans', 'Simplified Chinese'), ('zh-hant', 'Traditional Chinese'), ('zh-tw', 'Traditional Chinese')], default='en-us')),
                ('summary', models.TextField(null=True)),
                ('is_anonymous', models.BooleanField(default=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='posts')),
            ],
            options={
                'db_table': 'askbot_post',
            },
        ),
        migrations.CreateModel(
            name='PostFlagReason',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('added_at', models.DateTimeField()),
                ('title', models.CharField(max_length=128)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('details', models.ForeignKey(to='askbot.Post', related_name='post_reject_reasons')),
            ],
        ),
        migrations.CreateModel(
            name='PostRevision',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('revision', models.PositiveIntegerField()),
                ('revised_at', models.DateTimeField()),
                ('summary', models.CharField(max_length=300, blank=True)),
                ('text', models.TextField(blank=True)),
                ('approved', models.BooleanField(db_index=True, default=False)),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('by_email', models.BooleanField(default=False)),
                ('email_address', models.EmailField(max_length=254, blank=True, null=True)),
                ('title', models.CharField(max_length=300, blank=True, default='')),
                ('tagnames', models.CharField(max_length=125, blank=True, default='')),
                ('is_anonymous', models.BooleanField(default=False)),
                ('ip_addr', models.GenericIPAddressField(db_index=True, default='0.0.0.0')),
                ('approved_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='postrevisions')),
                ('post', models.ForeignKey(to='askbot.Post', blank=True, related_name='revisions', null=True)),
            ],
            options={
                'ordering': ('-revision',),
            },
        ),
        migrations.CreateModel(
            name='PostToGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('group', models.ForeignKey(to='askbot.Group')),
                ('post', models.ForeignKey(to='askbot.Post')),
            ],
            options={
                'db_table': 'askbot_post_groups',
            },
        ),
        migrations.CreateModel(
            name='QuestionView',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('when', models.DateTimeField()),
                ('question', models.ForeignKey(to='askbot.Post', related_name='viewed')),
                ('who', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='question_views')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionWidget',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('question_number', models.PositiveIntegerField(default=7)),
                ('tagnames', models.CharField(max_length=50, verbose_name='tags')),
                ('search_query', models.CharField(max_length=50, default='', blank=True, null=True)),
                ('order_by', models.CharField(max_length=18, choices=[('-added_at', 'date descendant'), ('added_at', 'date ascendant'), ('-last_activity_at', 'most recently active'), ('last_activity_at', 'least recently active'), ('-answer_count', 'more responses'), ('answer_count', 'fewer responses'), ('-points', 'more votes'), ('points', 'less votes')], default='-added_at')),
                ('style', models.TextField(verbose_name='css for the widget', blank=True, default="\n@import url('http://fonts.googleapis.com/css?family=Yanone+Kaffeesatz:300,400,700');\nbody {\n    overflow: hidden;\n}\n\n# container {\n    width: 200px;\n    height: 350px;\n}\nul {\n    list-style: none;\n    padding: 5px;\n    margin: 5px;\n}\nli {\n    border-bottom: # CCC 1px solid;\n    padding-bottom: 5px;\n    padding-top: 5px;\n}\nli:last-child {\n    border: none;\n}\na {\n    text-decoration: none;\n    color: # 464646;\n    font-family: 'Yanone Kaffeesatz', sans-serif;\n    font-size: 15px;\n}\n")),
                ('group', models.ForeignKey(to='askbot.Group', blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReplyAddress',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('address', models.CharField(unique=True, max_length=25)),
                ('reply_action', models.CharField(max_length=32, choices=[('post_answer', 'Post an answer'), ('post_comment', 'Post a comment'), ('replace_content', 'Edit post'), ('append_content', 'Append to post'), ('auto_answer_or_comment', 'Answer or comment, depending on the size of post'), ('validate_email', 'Validate email and record signature')], default='auto_answer_or_comment')),
                ('allowed_from_email', models.EmailField(max_length=150)),
                ('used_at', models.DateTimeField(default=None, null=True)),
                ('post', models.ForeignKey(to='askbot.Post', related_name='reply_addresses', null=True)),
                ('response_post', models.ForeignKey(to='askbot.Post', related_name='edit_addresses', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'askbot_replyaddress',
            },
        ),
        migrations.CreateModel(
            name='Repute',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('positive', models.SmallIntegerField(default=0)),
                ('negative', models.SmallIntegerField(default=0)),
                ('reputed_at', models.DateTimeField(default=datetime.datetime.now)),
                ('reputation_type', models.SmallIntegerField(choices=[(1, 'gain_by_upvoted'), (2, 'gain_by_answer_accepted'), (3, 'gain_by_accepting_answer'), (4, 'gain_by_downvote_canceled'), (5, 'gain_by_canceling_downvote'), (-1, 'lose_by_canceling_accepted_answer'), (-2, 'lose_by_accepted_answer_cancled'), (-3, 'lose_by_downvoted'), (-4, 'lose_by_flagged'), (-5, 'lose_by_downvoting'), (-6, 'lose_by_flagged_lastrevision_3_times'), (-7, 'lose_by_flagged_lastrevision_5_times'), (-8, 'lose_by_upvote_canceled'), (10, 'assigned_by_moderator')])),
                ('reputation', models.IntegerField(default=1)),
                ('comment', models.CharField(max_length=128, null=True)),
                ('question', models.ForeignKey(to='askbot.Post', blank=True, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'repute',
            },
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('group', models.CharField(max_length=100)),
                ('key', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=255, blank=True)),
                ('site', models.ForeignKey(verbose_name='Site', to='sites.Site')),
            ],
            bases=(models.Model, keyedcache.models.CachedObjectMixin),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('language_code', models.CharField(max_length=16, choices=[('af', 'Afrikaans'), ('ar', 'Arabic'), ('ast', 'Asturian'), ('az', 'Azerbaijani'), ('bg', 'Bulgarian'), ('be', 'Belarusian'), ('bn', 'Bengali'), ('br', 'Breton'), ('bs', 'Bosnian'), ('ca', 'Catalan'), ('cs', 'Czech'), ('cy', 'Welsh'), ('da', 'Danish'), ('de', 'German'), ('el', 'Greek'), ('en', 'English'), ('en-au', 'Australian English'), ('en-gb', 'British English'), ('eo', 'Esperanto'), ('es', 'Spanish'), ('es-ar', 'Argentinian Spanish'), ('es-mx', 'Mexican Spanish'), ('es-ni', 'Nicaraguan Spanish'), ('es-ve', 'Venezuelan Spanish'), ('et', 'Estonian'), ('eu', 'Basque'), ('fa', 'Persian'), ('fi', 'Finnish'), ('fr', 'French'), ('fy', 'Frisian'), ('ga', 'Irish'), ('gl', 'Galician'), ('he', 'Hebrew'), ('hi', 'Hindi'), ('hr', 'Croatian'), ('hu', 'Hungarian'), ('ia', 'Interlingua'), ('id', 'Indonesian'), ('io', 'Ido'), ('is', 'Icelandic'), ('it', 'Italian'), ('ja', 'Japanese'), ('ka', 'Georgian'), ('kk', 'Kazakh'), ('km', 'Khmer'), ('kn', 'Kannada'), ('ko', 'Korean'), ('lb', 'Luxembourgish'), ('lt', 'Lithuanian'), ('lv', 'Latvian'), ('mk', 'Macedonian'), ('ml', 'Malayalam'), ('mn', 'Mongolian'), ('mr', 'Marathi'), ('my', 'Burmese'), ('nb', 'Norwegian Bokmal'), ('ne', 'Nepali'), ('nl', 'Dutch'), ('nn', 'Norwegian Nynorsk'), ('os', 'Ossetic'), ('pa', 'Punjabi'), ('pl', 'Polish'), ('pt', 'Portuguese'), ('pt-br', 'Brazilian Portuguese'), ('ro', 'Romanian'), ('ru', 'Russian'), ('sk', 'Slovak'), ('sl', 'Slovenian'), ('sq', 'Albanian'), ('sr', 'Serbian'), ('sr-latn', 'Serbian Latin'), ('sv', 'Swedish'), ('sw', 'Swahili'), ('ta', 'Tamil'), ('te', 'Telugu'), ('th', 'Thai'), ('tr', 'Turkish'), ('tt', 'Tatar'), ('udm', 'Udmurt'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('vi', 'Vietnamese'), ('zh-cn', 'Simplified Chinese'), ('zh-hans', 'Simplified Chinese'), ('zh-hant', 'Traditional Chinese'), ('zh-tw', 'Traditional Chinese')], default='en-us')),
                ('status', models.SmallIntegerField(default=1)),
                ('used_count', models.PositiveIntegerField(default=0)),
                ('deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='created_tags')),
                ('deleted_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, related_name='deleted_tags', null=True)),
                ('suggested_by', models.ManyToManyField(help_text='Works only for suggested tags for tag moderation', to=settings.AUTH_USER_MODEL, related_name='suggested_tags')),
                ('tag_wiki', models.OneToOneField(to='askbot.Post', related_name='described_tag', null=True)),
            ],
            options={
                'db_table': 'tag',
                'ordering': ('-used_count', 'name'),
            },
        ),
        migrations.CreateModel(
            name='TagSynonym',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('source_tag_name', models.CharField(unique=True, max_length=255)),
                ('target_tag_name', models.CharField(max_length=255, db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('auto_rename_count', models.IntegerField(default=0)),
                ('last_auto_rename_at', models.DateTimeField(auto_now=True)),
                ('language_code', models.CharField(max_length=16, choices=[('af', 'Afrikaans'), ('ar', 'Arabic'), ('ast', 'Asturian'), ('az', 'Azerbaijani'), ('bg', 'Bulgarian'), ('be', 'Belarusian'), ('bn', 'Bengali'), ('br', 'Breton'), ('bs', 'Bosnian'), ('ca', 'Catalan'), ('cs', 'Czech'), ('cy', 'Welsh'), ('da', 'Danish'), ('de', 'German'), ('el', 'Greek'), ('en', 'English'), ('en-au', 'Australian English'), ('en-gb', 'British English'), ('eo', 'Esperanto'), ('es', 'Spanish'), ('es-ar', 'Argentinian Spanish'), ('es-mx', 'Mexican Spanish'), ('es-ni', 'Nicaraguan Spanish'), ('es-ve', 'Venezuelan Spanish'), ('et', 'Estonian'), ('eu', 'Basque'), ('fa', 'Persian'), ('fi', 'Finnish'), ('fr', 'French'), ('fy', 'Frisian'), ('ga', 'Irish'), ('gl', 'Galician'), ('he', 'Hebrew'), ('hi', 'Hindi'), ('hr', 'Croatian'), ('hu', 'Hungarian'), ('ia', 'Interlingua'), ('id', 'Indonesian'), ('io', 'Ido'), ('is', 'Icelandic'), ('it', 'Italian'), ('ja', 'Japanese'), ('ka', 'Georgian'), ('kk', 'Kazakh'), ('km', 'Khmer'), ('kn', 'Kannada'), ('ko', 'Korean'), ('lb', 'Luxembourgish'), ('lt', 'Lithuanian'), ('lv', 'Latvian'), ('mk', 'Macedonian'), ('ml', 'Malayalam'), ('mn', 'Mongolian'), ('mr', 'Marathi'), ('my', 'Burmese'), ('nb', 'Norwegian Bokmal'), ('ne', 'Nepali'), ('nl', 'Dutch'), ('nn', 'Norwegian Nynorsk'), ('os', 'Ossetic'), ('pa', 'Punjabi'), ('pl', 'Polish'), ('pt', 'Portuguese'), ('pt-br', 'Brazilian Portuguese'), ('ro', 'Romanian'), ('ru', 'Russian'), ('sk', 'Slovak'), ('sl', 'Slovenian'), ('sq', 'Albanian'), ('sr', 'Serbian'), ('sr-latn', 'Serbian Latin'), ('sv', 'Swedish'), ('sw', 'Swahili'), ('ta', 'Tamil'), ('te', 'Telugu'), ('th', 'Thai'), ('tr', 'Turkish'), ('tt', 'Tatar'), ('udm', 'Udmurt'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('vi', 'Vietnamese'), ('zh-cn', 'Simplified Chinese'), ('zh-hans', 'Simplified Chinese'), ('zh-hant', 'Traditional Chinese'), ('zh-tw', 'Traditional Chinese')], default='en-us')),
                ('owned_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='tag_synonyms')),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=300)),
                ('tagnames', models.CharField(max_length=125)),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('favourite_count', models.PositiveIntegerField(default=0)),
                ('answer_count', models.PositiveIntegerField(default=0)),
                ('last_activity_at', models.DateTimeField(default=datetime.datetime.now)),
                ('language_code', models.CharField(max_length=16, choices=[('af', 'Afrikaans'), ('ar', 'Arabic'), ('ast', 'Asturian'), ('az', 'Azerbaijani'), ('bg', 'Bulgarian'), ('be', 'Belarusian'), ('bn', 'Bengali'), ('br', 'Breton'), ('bs', 'Bosnian'), ('ca', 'Catalan'), ('cs', 'Czech'), ('cy', 'Welsh'), ('da', 'Danish'), ('de', 'German'), ('el', 'Greek'), ('en', 'English'), ('en-au', 'Australian English'), ('en-gb', 'British English'), ('eo', 'Esperanto'), ('es', 'Spanish'), ('es-ar', 'Argentinian Spanish'), ('es-mx', 'Mexican Spanish'), ('es-ni', 'Nicaraguan Spanish'), ('es-ve', 'Venezuelan Spanish'), ('et', 'Estonian'), ('eu', 'Basque'), ('fa', 'Persian'), ('fi', 'Finnish'), ('fr', 'French'), ('fy', 'Frisian'), ('ga', 'Irish'), ('gl', 'Galician'), ('he', 'Hebrew'), ('hi', 'Hindi'), ('hr', 'Croatian'), ('hu', 'Hungarian'), ('ia', 'Interlingua'), ('id', 'Indonesian'), ('io', 'Ido'), ('is', 'Icelandic'), ('it', 'Italian'), ('ja', 'Japanese'), ('ka', 'Georgian'), ('kk', 'Kazakh'), ('km', 'Khmer'), ('kn', 'Kannada'), ('ko', 'Korean'), ('lb', 'Luxembourgish'), ('lt', 'Lithuanian'), ('lv', 'Latvian'), ('mk', 'Macedonian'), ('ml', 'Malayalam'), ('mn', 'Mongolian'), ('mr', 'Marathi'), ('my', 'Burmese'), ('nb', 'Norwegian Bokmal'), ('ne', 'Nepali'), ('nl', 'Dutch'), ('nn', 'Norwegian Nynorsk'), ('os', 'Ossetic'), ('pa', 'Punjabi'), ('pl', 'Polish'), ('pt', 'Portuguese'), ('pt-br', 'Brazilian Portuguese'), ('ro', 'Romanian'), ('ru', 'Russian'), ('sk', 'Slovak'), ('sl', 'Slovenian'), ('sq', 'Albanian'), ('sr', 'Serbian'), ('sr-latn', 'Serbian Latin'), ('sv', 'Swedish'), ('sw', 'Swahili'), ('ta', 'Tamil'), ('te', 'Telugu'), ('th', 'Thai'), ('tr', 'Turkish'), ('tt', 'Tatar'), ('udm', 'Udmurt'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('vi', 'Vietnamese'), ('zh-cn', 'Simplified Chinese'), ('zh-hans', 'Simplified Chinese'), ('zh-hant', 'Traditional Chinese'), ('zh-tw', 'Traditional Chinese')], default='en-us')),
                ('closed', models.BooleanField(default=False)),
                ('closed_at', models.DateTimeField(blank=True, null=True)),
                ('close_reason', models.SmallIntegerField(blank=True, choices=[(1, 'duplicate question'), (2, 'question is off-topic or not relevant'), (3, 'too subjective and argumentative'), (4, 'not a real question'), (5, 'the question is answered, right answer was accepted'), (6, 'question is not relevant or outdated'), (7, 'question contains offensive or malicious remarks'), (8, 'spam or advertising'), (9, 'too localized')], null=True)),
                ('deleted', models.BooleanField(db_index=True, default=False)),
                ('approved', models.BooleanField(db_index=True, default=True)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('points', models.IntegerField(db_column='score', default=0)),
                ('accepted_answer', models.ForeignKey(to='askbot.Post', blank=True, related_name='+', null=True)),
                ('closed_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True)),
                ('favorited_by', models.ManyToManyField(through='askbot.FavoriteQuestion', to=settings.AUTH_USER_MODEL, related_name='unused_favorite_threads')),
                ('followed_by', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='followed_threads')),
            ],
        ),
        migrations.CreateModel(
            name='ThreadToGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('visibility', models.SmallIntegerField(choices=[(0, 'show only published responses'), (1, 'show all responses')], default=1)),
                ('group', models.ForeignKey(to='askbot.Group')),
                ('thread', models.ForeignKey(to='askbot.Thread')),
            ],
            options={
                'db_table': 'askbot_thread_groups',
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('vote', models.SmallIntegerField(choices=[(1, 'Up'), (-1, 'Down')])),
                ('voted_at', models.DateTimeField(default=datetime.datetime.now)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='votes')),
                ('voted_post', models.ForeignKey(to='askbot.Post', related_name='votes')),
            ],
            options={
                'db_table': 'vote',
            },
        ),
        migrations.AddField(
            model_name='thread',
            name='groups',
            field=models.ManyToManyField(through='askbot.ThreadToGroup', to='askbot.Group', related_name='group_threads'),
        ),
        migrations.AddField(
            model_name='thread',
            name='last_activity_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='unused_last_active_in_threads'),
        ),
        migrations.AddField(
            model_name='thread',
            name='tags',
            field=models.ManyToManyField(to='askbot.Tag', related_name='threads'),
        ),
        migrations.AddField(
            model_name='post',
            name='current_revision',
            field=models.ForeignKey(to='askbot.PostRevision', blank=True, related_name='rendered_posts', null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='deleted_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, related_name='deleted_posts', null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='endorsed_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, related_name='endorsed_posts', null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='groups',
            field=models.ManyToManyField(through='askbot.PostToGroup', to='askbot.Group', related_name='group_posts'),
        ),
        migrations.AddField(
            model_name='post',
            name='last_edited_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, related_name='last_edited_posts', null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='locked_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, related_name='locked_posts', null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='parent',
            field=models.ForeignKey(to='askbot.Post', blank=True, related_name='comments', null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='thread',
            field=models.ForeignKey(to='askbot.Thread', null=True, blank=True, related_name='posts', default=None),
        ),
        migrations.AddField(
            model_name='markedtag',
            name='tag',
            field=models.ForeignKey(to='askbot.Tag', related_name='user_selections'),
        ),
        migrations.AddField(
            model_name='markedtag',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='tag_selections'),
        ),
        migrations.AddField(
            model_name='importedobjectinfo',
            name='run',
            field=models.ForeignKey(to='askbot.ImportRun'),
        ),
        migrations.AddField(
            model_name='group',
            name='description',
            field=models.OneToOneField(to='askbot.Post', blank=True, related_name='described_group', null=True),
        ),
        migrations.AddField(
            model_name='favoritequestion',
            name='thread',
            field=models.ForeignKey(to='askbot.Thread'),
        ),
        migrations.AddField(
            model_name='favoritequestion',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='user_favorite_questions'),
        ),
        migrations.AddField(
            model_name='draftanswer',
            name='thread',
            field=models.ForeignKey(to='askbot.Thread', related_name='draft_answers'),
        ),
        migrations.AddField(
            model_name='bulktagsubscription',
            name='groups',
            field=models.ManyToManyField(to='askbot.Group'),
        ),
        migrations.AddField(
            model_name='bulktagsubscription',
            name='tags',
            field=models.ManyToManyField(to='askbot.Tag'),
        ),
        migrations.AddField(
            model_name='bulktagsubscription',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='award',
            name='badge',
            field=models.ForeignKey(to='askbot.BadgeData', related_name='award_badge'),
        ),
        migrations.AddField(
            model_name='award',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='award',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='award_user'),
        ),
        migrations.AddField(
            model_name='askwidget',
            name='group',
            field=models.ForeignKey(to='askbot.Group', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='askwidget',
            name='tag',
            field=models.ForeignKey(to='askbot.Tag', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='anonymousanswer',
            name='question',
            field=models.ForeignKey(to='askbot.Post', related_name='anonymous_answers'),
        ),
        migrations.AddField(
            model_name='activity',
            name='question',
            field=models.ForeignKey(to='askbot.Post', null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='recipients',
            field=models.ManyToManyField(through='askbot.ActivityAuditStatus', to=settings.AUTH_USER_MODEL, related_name='incoming_activity'),
        ),
        migrations.AddField(
            model_name='activity',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('user', 'voted_post')]),
        ),
        migrations.AlterUniqueTogether(
            name='threadtogroup',
            unique_together=set([('thread', 'group')]),
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set([('name', 'language_code')]),
        ),
        migrations.AlterUniqueTogether(
            name='setting',
            unique_together=set([('site', 'group', 'key')]),
        ),
        migrations.AlterUniqueTogether(
            name='posttogroup',
            unique_together=set([('post', 'group')]),
        ),
        migrations.AlterUniqueTogether(
            name='postrevision',
            unique_together=set([('post', 'revision')]),
        ),
        migrations.AlterUniqueTogether(
            name='longsetting',
            unique_together=set([('site', 'group', 'key')]),
        ),
        migrations.AlterUniqueTogether(
            name='emailfeedsetting',
            unique_together=set([('subscriber', 'feed_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='activityauditstatus',
            unique_together=set([('user', 'activity')]),
        ),
    ]
