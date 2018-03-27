# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from .models import Classes

# Create your views here.
def index(request):
    ordered_classes = Classes.objects.order_by('-cid')[:5]
    output = ', '.join([q.name for q in ordered_classes])
    return HttpResponse(output)

    #all_classes_list = Classes.objects.all()
    #return HttpResponse(all_classes_list)

# These don't work
def detail(request, cid_id):
    response = "you're looking at the results of class %s."
    return HttpResponse(response % cid_id)

def results(request, cid_id):
    response = "You're looking at the results of class %s."
    return HttpResponse(response % cid_id)

def vote(request, cid_id):
    return HttpResponse("You're voting on class %s." % cid_id)