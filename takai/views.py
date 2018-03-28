# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


from .models import Classes

# Create your views here.
def index(request):
    ordered_classes = Classes.objects.order_by('-cid')[:5]
    context = {'ordered_classes': ordered_classes}
    return render(request, 'takai/index.html', context)
    #output = ', '.join([q.name for q in ordered_classes])

def detail(request, cid):
    response = "you're looking at the results of class %s."
    return HttpResponse(response % cid)

def results(request, cid):
    response = "You're looking at the results of class %s."
    return HttpResponse(response % cid)

def vote(request, cid):
    return HttpResponse("You're voting on class %s." % cid)