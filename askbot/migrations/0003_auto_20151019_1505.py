# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('askbot', '0002_auto_20151019_0901'),
    ]

    operations = [
        migrations.CreateModel(
            name='AskWidget',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=100)),
                ('include_text_field', models.BooleanField(default=False)),
                ('inner_style', models.TextField(blank=True)),
                ('outer_style', models.TextField(blank=True)),
                ('group', models.ForeignKey(null=True, to='askbot.Group', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionWidget',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=100)),
                ('question_number', models.PositiveIntegerField(default=7)),
                ('tagnames', models.CharField(verbose_name='tags', max_length=50)),
                ('search_query', models.CharField(default='', blank=True, null=True, max_length=50)),
                ('order_by', models.CharField(default='-added_at', choices=[('-added_at', 'date descendant'), ('added_at', 'date ascendant'), ('-last_activity_at', 'most recently active'), ('last_activity_at', 'least recently active'), ('-answer_count', 'more responses'), ('answer_count', 'fewer responses'), ('-points', 'more votes'), ('points', 'less votes')], max_length=18)),
                ('style', models.TextField(default="\n@import url('http://fonts.googleapis.com/css?family=Yanone+Kaffeesatz:300,400,700');\nbody {\n    overflow: hidden;\n}\n\n#container {\n    width: 200px;\n    height: 350px;\n}\nul {\n    list-style: none;\n    padding: 5px;\n    margin: 5px;\n}\nli {\n    border-bottom: # CCC 1px solid;\n    padding-bottom: 5px;\n    padding-top: 5px;\n}\nli:last-child {\n    border: none;\n}\na {\n    text-decoration: none;\n    color: # 464646;\n    font-family: 'Yanone Kaffeesatz', sans-serif;\n    font-size: 15px;\n}\n", verbose_name='css for the widget', blank=True)),
                ('group', models.ForeignKey(null=True, to='askbot.Group', blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='language_code',
            field=models.CharField(default='ko-kr', choices=[('ko-kr', 'Korean'), ('en-us', 'English')], max_length=16),
        ),
        migrations.AlterField(
            model_name='tag',
            name='language_code',
            field=models.CharField(default='ko-kr', choices=[('ko-kr', 'Korean'), ('en-us', 'English')], max_length=16),
        ),
        migrations.AlterField(
            model_name='tagsynonym',
            name='language_code',
            field=models.CharField(default='ko-kr', choices=[('ko-kr', 'Korean'), ('en-us', 'English')], max_length=16),
        ),
        migrations.AlterField(
            model_name='thread',
            name='language_code',
            field=models.CharField(default='ko-kr', choices=[('ko-kr', 'Korean'), ('en-us', 'English')], max_length=16),
        ),
        migrations.AddField(
            model_name='askwidget',
            name='tag',
            field=models.ForeignKey(null=True, to='askbot.Tag', blank=True),
        ),
    ]
