# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-19 18:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='imageFile',
            field=models.CharField(default='Teleporter.png', max_length=50),
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='contentFile',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]