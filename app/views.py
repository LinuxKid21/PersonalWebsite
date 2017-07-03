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
from django.template import Context, Template
from django.http import HttpResponse

blog_template = '''
{% extends "app/main.html" %}
{% load static %}
{% load pygment_code %}
{% block content %}
    <p class = "page-title"> {{blogPage.title}} </p>
    <p style="margin-bottom: 0em; text-align: right;"> published: {{blogPage.publication_date}} {{blogPage.publication_time}} PST/PDT</p>
    {% if blogPage.edited %}
        <p style="margin-bottom: 0em; text-align: right;"> last edited: {{blogPage.edit_date}} {{blogPage.edit_time}} PST/PDT</p>
    {% endif %}'''


blog_template_preview = '''
{% extends "app/main.html" %}
{% load static %}
{% load pygment_code %}

{% block content %}
    <p style = "margin-top: 80px;"> this is a preview page.
        {% if blogPage.published %}
            It has been <b>published</b>. See the published page <a href = "{% url "blog" blogPage.id %}">here</a>
        {% else %}
            It is just a <b>draft</b>.
        {% endif %}
        <form action="{% url 'main' 'admin/update' %}" method="post">
            <input type="hidden" name="pageID" value = "{{blogPage.id}}">
            <input type="submit" value = "go back and edit">
            {% csrf_token %}
        </form>
    </p>
    
        
    <p class = "page-title"> {{blogPage.title}} </p>
    <p style="margin-bottom: 0em; text-align: right;"> published: {{blogPage.publication_date}} {{blogPage.publication_time}} PST/PDT</p>
    {% if blogPage.edited %}
        <p style="margin-bottom: 0em; text-align: right;"> last edited: {{blogPage.edit_date}} {{blogPage.edit_time}} PST/PDT</p>
    {% endif %}'''

blog_template_ending = '{% endblock %}'



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
    template = Template(blog_template + page.content + blog_template_ending)
    context = RequestContext(request, {'blogPage': page,
        'loggedin' : request.user.is_authenticated})
    # return renderPageRequested(request, 'app/blog/blog_template.html',
    #     {'blogPage': page,
    #     'loggedin' : request.user.is_authenticated})
    return HttpResponse(template.render(context))

def blog_index(request, tag_name):
    pages = BlogPage.objects.order_by('-publication_date', '-publication_time')
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
        page.imageFile = image
        page.tag = tag
        page.published = (status == 'Published')
        # summary is first 500 words of content with all paragrap tags, video tags, headers(and their content), django templates, and images removed. More to come...
        page.summary = re.sub(r'(?:<p[\s\S]*?>|</p>|<video[\s\S]*?>[\s\S]*?</video>|<h1[\s\S]*?>[\s\S]*?</h1>|<h2[\s\S]*?>[\s\S]*?</h2>|<h3[\s\S]*?>[\s\S]*?</h3>|<img[\s\S]*?/>|{%[\s\S]*?%})', '', content[0:1000])[0:500] + '...'
        page.save()
        
        
        template = Template(blog_template_preview + page.content + blog_template_ending)
        context = RequestContext(request, {'blogPage': page,
            'loggedin' : request.user.is_authenticated})
        return HttpResponse(template.render(context))
        # return renderPageRequested(request, 'app/admin/preview.html', {'blogPage' : page})
        
    elif(page_id == 'delete'):
        pageId = request.POST.get('pageID', 'INVALID')
        if(pageId == 'INVALID'):
            return  renderPageRequested(request, 'app/pages/notfound.html')
        
        page = BlogPage.objects.get(id = pageId)
        page.delete()
        return renderPageRequested(request, 'app/admin/deleted.html')
        
    else:
        return renderPageRequested(request, 'app/pages/notfound.html')
