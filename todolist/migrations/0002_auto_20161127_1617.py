# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-28 00:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todolist', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grouptask',
            name='assignee',
        ),
        migrations.AddField(
            model_name='grouptask',
            name='assignee',
            field=models.ManyToManyField(blank=True, null=True, related_name='assignedTo', to=settings.AUTH_USER_MODEL),
        ),
    ]
