# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from .models import Classes

# Create your views here.
def index(request):
    all_classes_list = Classes.objects.all()
    return HttpResponse(all_classes_list)
