"""
Definition of views.
"""

from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from DjangoApp import settings
from os import path
import os
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import uuid
import re


def renderPageRequested(request, page_id, context={}):
    """Renders the main page."""
    assert isinstance(request, HttpRequest)
    
    # add loggedin variable required by the base template
    context.update({'loggedin' : request.user.is_authenticated})
    return render(
        request,
        page_id,
        context
    )

def main(request, page_id):
    """Renders the main page."""
    assert isinstance(request, HttpRequest)
    
    if(not path.isfile(path.join(settings.PROJECT_ROOT, 'app/templates/app/pages/', page_id))):
        return renderPageRequested(request, 'app/pages/notfound.html')
    
    return renderPageRequested(request, 'app/pages/' + page_id)


def emptyURL(request):
    return renderPageRequested(request, 'app/pages/home.html')
    
def blog(request, page_id):
    page = get_object_or_404(BlogPage, pk=page_id)
    return renderPageRequested(request, 'app/blog/blog_template.html',
        {'blogPage': page})

def blog_index(request, tag_name):
    pages = BlogPage.objects.order_by('publication_date', 'publication_time')
    if(not tag_name):
        return renderPageRequested(request, 'app/blog/blog_index.html',
            {'blogPages': pages,
            'tag_name' : tag_name,
            'admin' : request.user.is_authenticated})
    else:
        tag_name = tag_name.lower()
        return renderPageRequested(request, 'app/blog/blog_index.html',
            {'blogPages': pages.filter(tag = tag_name),
            'tag_name' : tag_name,
            'admin' : request.user.is_authenticated})

def invalidURL(request):
    return renderPageRequested(request, 'app/pages/notfound.html')






@login_required
def myAdmin(request, page_id):
    if(not page_id):
        return renderPageRequested(request, 'app/admin/admin.html')
        
        
    elif(page_id == 'logout'):
        logout(request)
        return renderPageRequested(request, 'app/admin/logout.html')
        
        
    elif(page_id == 'CreatePost'):
        newPage = BlogPage.objects.create(title = 'default-title', summary = '', content = '', tag = 'Project')
        newPage.save()
        return renderPageRequested(request, 'app/admin/editPost.html', {'editPage' : newPage})
        
        
    elif(page_id == 'update'):
        pageId = request.POST.get('pageID', 'INVALID')
        if(pageId == 'INVALID'):
            return  renderPageRequested(request, 'app/pages/notfound.html')
        page = BlogPage.objects.get(id = pageId)
        return renderPageRequested(request, 'app/admin/editPost.html', {'editPage' : page})
        
        
        
    elif(page_id == 'publish'):
        title = request.POST.get('title', 'default-title')
        image = request.POST.get('image', 'Teleporter.png')
        tag = request.POST.get('tag', 'project')
        status = request.POST.get('status', 'Draft')
        content = request.POST.get('content', 'insert code here')
        pageId = request.POST.get('pageID', 'INVALID')
        if(pageId == 'INVALID'):
            return  renderPageRequested(request, 'app/pages/notfound.html')
        
        page = BlogPage.objects.get(id = pageId)
        page.content = content
        page.title = title
        page.image = image
        page.tag = tag
        page.published = (status == 'Published')
        # summary is first 500 words of content with all paragrap tags, headers(and their content) and images removed. More to come...
        page.summary = re.sub(r'(?:<p[\s\S]*?>|</p>|<h1>[\s\S]*?</h1>|<h2>[\s\S]*?</h2>|<h3>[\s\S]*?</h3>|<img[\s\S]*?/>)', '', content[0:1000])[0:500]
        page.save()
        
        return renderPageRequested(request, 'app/admin/preview.html', {'blogPage' : page})
        
    elif(page_id == 'delete'):
        pageId = request.POST.get('pageID', 'INVALID')
        if(pageId == 'INVALID'):
            return  renderPageRequested(request, 'app/pages/notfound.html')
        
        page = BlogPage.objects.get(id = pageId)
        page.delete()
        return renderPageRequested(request, 'app/admin/deleted.html')
        
    else:
        return renderPageRequested(request, 'app/pages/notfound.html')
