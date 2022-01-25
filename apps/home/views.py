# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .forms import TrendsRequest
from .tasks import extract_trends
 


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def google_trends(request):
    if request.method =='POST':
        form = TrendsRequest(request.POST)
        if form.is_valid():
            keywords = form.cleaned_data['keywords'].split(',')
            result = extract_trends.delay(keywords, 'now 1-d')
            _form = TrendsRequest()
            context ={
                'task_id':result.task_id,
                'form' : _form,
                #'keywords': result

                }
            
            return render(request, "home/index.html", context )
    else:
        _form = TrendsRequest()
        context = {
            'form':_form,
            }
        return render(request, "home/index.html", context )

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
