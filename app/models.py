"""
Definition of models.
"""

from django.db import models
from DjangoApp import settings
from os import path
from django.contrib import admin
import datetime

class BlogPage(models.Model):
    publication_date = models.DateField(auto_now_add=True)
    publication_time = models.TimeField(auto_now_add=True)
    edit_date = models.DateField(auto_now=True)
    edit_time = models.TimeField(auto_now=True)
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=500)
    contentFile = models.CharField(max_length=50, primary_key=True)
    tag = models.CharField(max_length=15) # something like Project or Blog
    imageFile = models.CharField(max_length=50, default='Teleporter.png')
    published = models.BooleanField(default=False)
    def __str__(self):
        return self.title + ' -------- ' + self.tag
    @property
    def edited(self):
        return abs((datetime.datetime.combine(self.publication_date, self.publication_time) - datetime.datetime.combine(self.edit_date, self.edit_time)).total_seconds()) > 1



admin.site.register(BlogPage)
