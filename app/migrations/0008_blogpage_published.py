# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-31 05:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20170529_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]