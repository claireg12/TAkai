# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


from .models import Classes

# Create your views here.

#def detail(request, cid):
#    try:
#        some_class = Classes.objects.get(pk=cid)
#    except Classes.DoesNotExist:
#        raise Http404("Class does not exist")
#    return render(request, 'takai/detail.html', {'some_class': some_class})

def semester(request, year, semester):
    ordered_classes = Classes.objects.order_by('-cid')
    current_classes = ordered_classes.filter(session__semester='Spring', session__year=2018)
    context = {'current_classes': current_classes, 'year': year, 'semester':semester}
    return render(request, 'takai/index.html', context)

def session(request, year, semester, cid):
    try:
        some_class = Classes.objects.get(pk=cid)
    except Classes.DoesNotExist:
        raise Http404("Class does not exist")
    return render(request, 'takai/detail.html', {'some_class': some_class})