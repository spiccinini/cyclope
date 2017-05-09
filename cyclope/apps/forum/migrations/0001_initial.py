# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-05-08 22:51
from __future__ import unicode_literals

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=250, verbose_name='name')),
                ('slug', autoslug.fields.AutoSlugField(blank=True, editable=True, populate_from=b'name', unique=True)),
                ('published', models.BooleanField(default=True, verbose_name='published')),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='creation date')),
                ('modification_date', models.DateTimeField(auto_now=True, verbose_name='modification date')),
                ('allow_comments', models.CharField(choices=[(b'SITE', 'default'), (b'YES', 'enabled'), (b'NO', 'disabled')], default=b'SITE', max_length=4, verbose_name='allow comments')),
                ('show_author', models.CharField(choices=[(b'AUTHOR', 'author'), (b'USER', 'user if author is empty'), (b'SITE', 'default')], default=b'SITE', help_text='Select which field to use to show as author of this content.', max_length=6, verbose_name='show author')),
                ('text', models.TextField(verbose_name='text')),
                ('anonymous_name', models.CharField(blank=True, default=b'', help_text='your name', max_length=50, verbose_name='name')),
                ('user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-creation_date',),
                'verbose_name': 'topic',
                'verbose_name_plural': 'topics',
            },
        ),
    ]
