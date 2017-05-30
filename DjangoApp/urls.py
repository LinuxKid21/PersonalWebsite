"""
Definition of urls for DjangoApp.
"""

from datetime import datetime
from django.conf.urls import url
from app.views import *
from app.models import *
from django.contrib.auth import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', emptyURL, name='emptyURL'),
    
    url(r'^index/(?P<tag_name>[\S]*)$', blog_index, name='blog_index'),
    url(r'^blog/(?P<page_id>[\S]+)$', blog, name='blog'),
    
    url(r'^admin/(?P<page_id>[\S]*)$', myAdmin, name='admin'),
    
    url(r'^login', views.login, name='login'), #automagically loads template 'registration/login.html'
    
    # something like: website-url/page-id.html
    # matches all non-space characters
    url(r'^(?P<page_id>[\S]+)$', main, name='main'),
    
]
