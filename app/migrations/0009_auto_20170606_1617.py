# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-06 23:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_blogpage_published'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpage',
            name='contentFile',
        ),
        migrations.AddField(
            model_name='blogpage',
            name='content',
            field=models.TextField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blogpage',
            name='id',
            field=models.AutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]