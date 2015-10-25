# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import picklefield.fields
from django.conf import settings
import djorm_pgfulltext.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_auto_20151021_1610'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('activity_type', models.SmallIntegerField(db_index=True, choices=[(1, 'asked a question'), (2, 'answered a question'), (3, 'commented question'), (4, 'commented answer'), (5, 'edited question'), (6, 'edited answer'), (7, 'received badge'), (8, 'marked best answer'), (9, 'upvoted'), (10, 'downvoted'), (11, 'canceled vote'), (12, 'deleted question'), (13, 'deleted answer'), (14, 'marked offensive'), (15, 'updated tags'), (16, 'selected favorite'), (17, 'completed user profile'), (18, 'email update sent to user'), (29, 'a post was shared'), (20, 'reminder about unanswered questions sent'), (21, 'reminder about accepting the best answer sent'), (19, 'mentioned in the post'), (22, 'created tag description'), (23, 'updated tag description'), (24, 'made a new post'), (25, 'made an edit'), (26, 'created post reject reason'), (27, 'updated post reject reason'), (28, 'sent email address validation message'), (31, 'sent moderation alert')])),
                ('active_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('object_id', models.PositiveIntegerField(db_index=True)),
                ('is_auditted', models.BooleanField(default=False)),
                ('summary', models.TextField(default='')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='ActivityAuditStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('status', models.SmallIntegerField(default=0, choices=[(0, 'new'), (1, 'seen')])),
                ('activity', models.ForeignKey(to='askbot.Activity')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AnonymousAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('session_key', models.CharField(max_length=40)),
                ('wiki', models.BooleanField(default=False)),
                ('added_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('ip_addr', models.GenericIPAddressField()),
                ('text', models.TextField()),
                ('author', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AnonymousQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('session_key', models.CharField(max_length=40)),
                ('wiki', models.BooleanField(default=False)),
                ('added_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('ip_addr', models.GenericIPAddressField()),
                ('text', models.TextField()),
                ('title', models.CharField(max_length=300)),
                ('tagnames', models.CharField(max_length=125)),
                ('is_anonymous', models.BooleanField(default=False)),
                ('author', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AskWidget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=100)),
                ('include_text_field', models.BooleanField(default=False)),
                ('inner_style', models.TextField(blank=True)),
                ('outer_style', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('object_id', models.PositiveIntegerField()),
                ('awarded_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('notified', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='BadgeData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('slug', models.SlugField(unique=True)),
                ('awarded_count', models.PositiveIntegerField(default=0)),
                ('display_order', models.PositiveIntegerField(default=0)),
                ('awarded_to', models.ManyToManyField(through='askbot.Award', related_name='badges', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('display_order', 'slug'),
            },
        ),
        migrations.CreateModel(
            name='BulkTagSubscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('date_added', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='DraftAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('text', models.TextField(null=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='draft_answers')),
            ],
        ),
        migrations.CreateModel(
            name='DraftQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(null=True, max_length=300)),
                ('text', models.TextField(null=True)),
                ('tagnames', models.CharField(null=True, max_length=125)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmailFeedSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('feed_type', models.CharField(choices=[('q_all', 'Entire forum'), ('q_ask', 'Questions that I asked'), ('q_ans', 'Questions that I answered'), ('q_sel', 'Individually selected questions'), ('m_and_c', 'Mentions and comment responses')], max_length=16)),
                ('frequency', models.CharField(default='n', choices=[('i', 'instantly'), ('d', 'daily'), ('w', 'weekly'), ('n', 'no email')], max_length=8)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('reported_at', models.DateTimeField(null=True)),
                ('subscriber', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='notification_subscriptions')),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('added_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('group_ptr', models.OneToOneField(parent_link=True, serialize=False, to='auth.Group', primary_key=True, auto_created=True)),
                ('logo_url', models.URLField(null=True)),
                ('moderate_email', models.BooleanField(default=True)),
                ('moderate_answers_to_enquirers', models.BooleanField(default=False, help_text='If true, answers to outsiders questions will be shown to the enquirers only when selected by the group moderators.')),
                ('openness', models.SmallIntegerField(default=2, choices=[(0, 'open'), (1, 'moderated'), (2, 'closed')])),
                ('preapproved_emails', models.TextField(null=True, default='', blank=True)),
                ('preapproved_email_domains', models.TextField(null=True, default='', blank=True)),
                ('is_vip', models.BooleanField(default=False, help_text='Check to make members of this group site moderators')),
                ('read_only', models.BooleanField(default=False)),
            ],
            bases=('auth.group',),
        ),
        migrations.CreateModel(
            name='GroupMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('level', models.SmallIntegerField(default=1, choices=[(0, 'pending'), (1, 'full')])),
                ('group', models.ForeignKey(to='auth.Group')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ImportedObjectInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('old_id', models.IntegerField(help_text='Old object id in the source database')),
                ('new_id', models.IntegerField(help_text='New object id in the current database')),
                ('model', models.CharField(default='', help_text='dotted python path to model', max_length=255)),
                ('extra_info', picklefield.fields.PickledObjectField(editable=False, help_text='to hold dictionary for various data')),
            ],
        ),
        migrations.CreateModel(
            name='ImportRun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('command', models.TextField(default='')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MarkedTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('reason', models.CharField(choices=[('good', 'interesting'), ('bad', 'ignored'), ('subscribed', 'subscribed')], max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('message', models.TextField(verbose_name='message')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='_message_set')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('post_type', models.CharField(db_index=True, max_length=255)),
                ('old_question_id', models.PositiveIntegerField(null=True, default=None, unique=True, blank=True)),
                ('old_answer_id', models.PositiveIntegerField(null=True, default=None, unique=True, blank=True)),
                ('old_comment_id', models.PositiveIntegerField(null=True, default=None, unique=True, blank=True)),
                ('added_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('endorsed', models.BooleanField(db_index=True, default=False)),
                ('endorsed_at', models.DateTimeField(null=True, blank=True)),
                ('approved', models.BooleanField(db_index=True, default=True)),
                ('deleted', models.BooleanField(db_index=True, default=False)),
                ('deleted_at', models.DateTimeField(null=True, blank=True)),
                ('wiki', models.BooleanField(default=False)),
                ('wikified_at', models.DateTimeField(null=True, blank=True)),
                ('locked', models.BooleanField(default=False)),
                ('locked_at', models.DateTimeField(null=True, blank=True)),
                ('points', models.IntegerField(default=0, db_column='score')),
                ('vote_up_count', models.IntegerField(default=0)),
                ('vote_down_count', models.IntegerField(default=0)),
                ('comment_count', models.PositiveIntegerField(default=0)),
                ('offensive_flag_count', models.SmallIntegerField(default=0)),
                ('last_edited_at', models.DateTimeField(null=True, blank=True)),
                ('html', models.TextField(null=True)),
                ('text', models.TextField(null=True)),
                ('language_code', models.CharField(default='ko-kr', choices=[('ko-kr', 'Korean'), ('en-us', 'English')], max_length=16)),
                ('summary', models.TextField(null=True)),
                ('is_anonymous', models.BooleanField(default=False)),
                ('search_index', djorm_pgfulltext.fields.VectorField(null=True, default='', serialize=False, db_index=True, editable=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='posts')),
            ],
        ),
        migrations.CreateModel(
            name='PostFlagReason',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('added_at', models.DateTimeField()),
                ('title', models.CharField(max_length=128)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('details', models.ForeignKey(to='askbot.Post', related_name='post_reject_reasons')),
            ],
        ),
        migrations.CreateModel(
            name='PostRevision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('revision', models.PositiveIntegerField()),
                ('revised_at', models.DateTimeField()),
                ('summary', models.CharField(max_length=300, blank=True)),
                ('text', models.TextField(blank=True)),
                ('approved', models.BooleanField(db_index=True, default=False)),
                ('approved_at', models.DateTimeField(null=True, blank=True)),
                ('by_email', models.BooleanField(default=False)),
                ('email_address', models.EmailField(null=True, max_length=254, blank=True)),
                ('title', models.CharField(default='', max_length=300, blank=True)),
                ('tagnames', models.CharField(default='', max_length=125, blank=True)),
                ('is_anonymous', models.BooleanField(default=False)),
                ('ip_addr', models.GenericIPAddressField(db_index=True, default='0.0.0.0')),
                ('approved_by', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, blank=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='postrevisions')),
                ('post', models.ForeignKey(null=True, to='askbot.Post', related_name='revisions', blank=True)),
            ],
            options={
                'ordering': ('-revision',),
            },
        ),
        migrations.CreateModel(
            name='PostToGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('group', models.ForeignKey(to='askbot.Group')),
                ('post', models.ForeignKey(to='askbot.Post')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionView',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('when', models.DateTimeField()),
                ('question', models.ForeignKey(to='askbot.Post', related_name='viewed')),
                ('who', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='question_views')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionWidget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=100)),
                ('question_number', models.PositiveIntegerField(default=7)),
                ('tagnames', models.CharField(verbose_name='tags', max_length=50)),
                ('search_query', models.CharField(null=True, default='', max_length=50, blank=True)),
                ('order_by', models.CharField(default='-added_at', choices=[('-added_at', 'date descendant'), ('added_at', 'date ascendant'), ('-last_activity_at', 'most recently active'), ('last_activity_at', 'least recently active'), ('-answer_count', 'more responses'), ('answer_count', 'fewer responses'), ('-points', 'more votes'), ('points', 'less votes')], max_length=18)),
                ('style', models.TextField(verbose_name='css for the widget', default="\n@import url('http://fonts.googleapis.com/css?family=Yanone+Kaffeesatz:300,400,700');\nbody {\n    overflow: hidden;\n}\n\n#container {\n    width: 200px;\n    height: 350px;\n}\nul {\n    list-style: none;\n    padding: 5px;\n    margin: 5px;\n}\nli {\n    border-bottom: # CCC 1px solid;\n    padding-bottom: 5px;\n    padding-top: 5px;\n}\nli:last-child {\n    border: none;\n}\na {\n    text-decoration: none;\n    color: # 464646;\n    font-family: 'Yanone Kaffeesatz', sans-serif;\n    font-size: 15px;\n}\n", blank=True)),
                ('group', models.ForeignKey(null=True, to='askbot.Group', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReplyAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('address', models.CharField(unique=True, max_length=25)),
                ('reply_action', models.CharField(default='auto_answer_or_comment', choices=[('post_answer', 'Post an answer'), ('post_comment', 'Post a comment'), ('replace_content', 'Edit post'), ('append_content', 'Append to post'), ('auto_answer_or_comment', 'Answer or comment, depending on the size of post'), ('validate_email', 'Validate email and record signature')], max_length=32)),
                ('allowed_from_email', models.EmailField(max_length=150)),
                ('used_at', models.DateTimeField(null=True, default=None)),
                ('post', models.ForeignKey(null=True, to='askbot.Post', related_name='reply_addresses')),
                ('response_post', models.ForeignKey(null=True, to='askbot.Post', related_name='edit_addresses')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Repute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('positive', models.SmallIntegerField(default=0)),
                ('negative', models.SmallIntegerField(default=0)),
                ('reputed_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('reputation_type', models.SmallIntegerField(choices=[(1, 'gain_by_upvoted'), (2, 'gain_by_answer_accepted'), (3, 'gain_by_accepting_answer'), (4, 'gain_by_downvote_canceled'), (5, 'gain_by_canceling_downvote'), (-1, 'lose_by_canceling_accepted_answer'), (-2, 'lose_by_accepted_answer_cancled'), (-3, 'lose_by_downvoted'), (-4, 'lose_by_flagged'), (-5, 'lose_by_downvoting'), (-6, 'lose_by_flagged_lastrevision_3_times'), (-7, 'lose_by_flagged_lastrevision_5_times'), (-8, 'lose_by_upvote_canceled'), (10, 'assigned_by_moderator')])),
                ('reputation', models.IntegerField(default=1)),
                ('comment', models.CharField(null=True, max_length=128)),
                ('question', models.ForeignKey(null=True, to='askbot.Post', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('language_code', models.CharField(default='ko-kr', choices=[('ko-kr', 'Korean'), ('en-us', 'English')], max_length=16)),
                ('status', models.SmallIntegerField(default=1)),
                ('used_count', models.PositiveIntegerField(default=0)),
                ('deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(null=True, blank=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='created_tags')),
                ('deleted_by', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, related_name='deleted_tags', blank=True)),
                ('suggested_by', models.ManyToManyField(help_text='Works only for suggested tags for tag moderation', to=settings.AUTH_USER_MODEL, related_name='suggested_tags')),
                ('tag_wiki', models.OneToOneField(null=True, to='askbot.Post', related_name='described_tag')),
            ],
            options={
                'ordering': ('-used_count', 'name'),
            },
        ),
        migrations.CreateModel(
            name='TagSynonym',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('source_tag_name', models.CharField(unique=True, max_length=255)),
                ('target_tag_name', models.CharField(db_index=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('auto_rename_count', models.IntegerField(default=0)),
                ('last_auto_rename_at', models.DateTimeField(auto_now=True)),
                ('language_code', models.CharField(default='ko-kr', choices=[('ko-kr', 'Korean'), ('en-us', 'English')], max_length=16)),
                ('owned_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='tag_synonyms')),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=300)),
                ('tagnames', models.CharField(max_length=125)),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('favourite_count', models.PositiveIntegerField(default=0)),
                ('answer_count', models.PositiveIntegerField(default=0)),
                ('last_activity_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('language_code', models.CharField(default='ko-kr', choices=[('ko-kr', 'Korean'), ('en-us', 'English')], max_length=16)),
                ('closed', models.BooleanField(default=False)),
                ('closed_at', models.DateTimeField(null=True, blank=True)),
                ('close_reason', models.SmallIntegerField(null=True, choices=[(1, 'duplicate question'), (2, 'question is off-topic or not relevant'), (3, 'too subjective and argumentative'), (4, 'not a real question'), (5, 'the question is answered, right answer was accepted'), (6, 'question is not relevant or outdated'), (7, 'question contains offensive or malicious remarks'), (8, 'spam or advertising'), (9, 'too localized')], blank=True)),
                ('deleted', models.BooleanField(db_index=True, default=False)),
                ('approved', models.BooleanField(db_index=True, default=True)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('points', models.IntegerField(default=0, db_column='score')),
                ('search_index', djorm_pgfulltext.fields.VectorField(null=True, default='', serialize=False, db_index=True, editable=False)),
                ('accepted_answer', models.ForeignKey(null=True, to='askbot.Post', related_name='+', blank=True)),
                ('closed_by', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, blank=True)),
                ('favorited_by', models.ManyToManyField(through='askbot.FavoriteQuestion', related_name='unused_favorite_threads', to=settings.AUTH_USER_MODEL)),
                ('followed_by', models.ManyToManyField(related_name='followed_threads', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ThreadToGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('visibility', models.SmallIntegerField(default=1, choices=[(0, 'show only published responses'), (1, 'show all responses')])),
                ('group', models.ForeignKey(to='askbot.Group')),
                ('thread', models.ForeignKey(to='askbot.Thread')),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('vote', models.SmallIntegerField(choices=[(1, 'Up'), (-1, 'Down')])),
                ('voted_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='votes')),
                ('voted_post', models.ForeignKey(to='askbot.Post', related_name='votes')),
            ],
        ),
        migrations.AddField(
            model_name='thread',
            name='groups',
            field=models.ManyToManyField(through='askbot.ThreadToGroup', related_name='group_threads', to='askbot.Group'),
        ),
        migrations.AddField(
            model_name='thread',
            name='last_activity_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='unused_last_active_in_threads'),
        ),
        migrations.AddField(
            model_name='thread',
            name='tags',
            field=models.ManyToManyField(related_name='threads', to='askbot.Tag'),
        ),
        migrations.AddField(
            model_name='post',
            name='current_revision',
            field=models.ForeignKey(null=True, to='askbot.PostRevision', related_name='rendered_posts', blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='deleted_by',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, related_name='deleted_posts', blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='endorsed_by',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, related_name='endorsed_posts', blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='groups',
            field=models.ManyToManyField(through='askbot.PostToGroup', related_name='group_posts', to='askbot.Group'),
        ),
        migrations.AddField(
            model_name='post',
            name='last_edited_by',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, related_name='last_edited_posts', blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='locked_by',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, related_name='locked_posts', blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='parent',
            field=models.ForeignKey(null=True, to='askbot.Post', related_name='comments', blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='thread',
            field=models.ForeignKey(null=True, default=None, to='askbot.Thread', related_name='posts', blank=True),
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
            field=models.OneToOneField(null=True, to='askbot.Post', related_name='described_group', blank=True),
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
            field=models.ForeignKey(null=True, to='askbot.Group', blank=True),
        ),
        migrations.AddField(
            model_name='askwidget',
            name='tag',
            field=models.ForeignKey(null=True, to='askbot.Tag', blank=True),
        ),
        migrations.AddField(
            model_name='anonymousanswer',
            name='question',
            field=models.ForeignKey(to='askbot.Post', related_name='anonymous_answers'),
        ),
        migrations.AddField(
            model_name='activity',
            name='question',
            field=models.ForeignKey(null=True, to='askbot.Post'),
        ),
        migrations.AddField(
            model_name='activity',
            name='recipients',
            field=models.ManyToManyField(through='askbot.ActivityAuditStatus', related_name='incoming_activity', to=settings.AUTH_USER_MODEL),
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
            name='posttogroup',
            unique_together=set([('post', 'group')]),
        ),
        migrations.AlterUniqueTogether(
            name='postrevision',
            unique_together=set([('post', 'revision')]),
        ),
        migrations.AlterUniqueTogether(
            name='groupmembership',
            unique_together=set([('group', 'user')]),
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
