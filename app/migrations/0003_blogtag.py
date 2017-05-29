# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-29 22:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20170519_1132'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('blogPage', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.BlogPage')),
            ],
        ),
    ]
