"""
Definition of views.
"""

from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from DjangoApp import settings
from os import path
from .models import BlogPage


def renderPageRequested(request, page_id, context={}):
    """Renders the main page."""
    assert isinstance(request, HttpRequest)
    
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
    if(not path.isfile(path.join(settings.PROJECT_ROOT, 'app/templates/app/blog/', page_id))):
        return renderPageRequested(request, 'app/pages/notfound.html')
    
    page = get_object_or_404(BlogPage, pk=page_id)
    return renderPageRequested(request, 'app/blog/' + page_id,
        {'blogPage': page})

def blog_index(request):
    pages = BlogPage.objects.order_by('publication_date', 'publication_time')
    return renderPageRequested(request, 'app/blog/blog_index.html',
        {'blogPages': pages})

def invalidURL(request):
    return renderPageRequested(request, 'app/pages/notfound.html')

