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
    imageFile = models.CharField(max_length=50, default='Teleporter.png')
    def __str__(self):
        return self.title
    
    @property
    def edited(self):
        return abs((datetime.datetime.combine(self.publication_date, self.publication_time) - datetime.datetime.combine(self.edit_date, self.edit_time)).total_seconds()) > 1


class BlogTag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=15)
    blogPage = models.ForeignKey('BlogPage', on_delete=models.CASCADE)
    def __str__(self):
        return self.name + ' -------- ' + str(self.blogPage)


admin.site.register(BlogPage)
admin.site.register(BlogTag)
