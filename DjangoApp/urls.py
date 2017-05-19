"""
Definition of urls for DjangoApp.
"""

from datetime import datetime
from django.conf.urls import url
from app.views import *
from app.models import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', emptyURL, name='emptyURL'),
    
    url(r'^blog/index.html$', blog_index, name='blog_index'),
    url(r'^blog/$', blog_index, name='blog_index'),
    
    url(r'^blog/(?P<page_id>[\S]+)$', blog, name='blog'),
    # url(r'^project/(?P<page_id>[\S]+)$', project, name='project'),
    
    url(r'^admin/', admin.site.urls),
    
    # something like: website-url/page-id.html
    # matches all non-space characters
    url(r'^(?P<page_id>[\S]+)$', main, name='main'),
]
