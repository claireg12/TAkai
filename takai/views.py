# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Classes, Students, Teach, Professors

# Home page
def semester(request, year, semester):
    ordered_classes = Classes.objects.order_by('cid')
    current_classes = ordered_classes.filter(session__semester=semester, session__year=year)
    context = {'current_classes': current_classes, 'year': year, 'semester':semester}
    return render(request, 'takai/semester.html', context)

# Course page
def session(request, year, semester, cid):
    try:
        some_class = Classes.objects.get(pk=cid)
        teach = Teach.objects.filter(cid=cid, semester=semester, year=year).values_list('fid', flat=True)
        # this_teach = teach[0].professors_fid
        # names = Professors.objects.filter(fid=this_teach)
        # prof = teach.filter(professors_fid=teach.fid)
        # profs = Professors.filter(fid=)
        context = {'some_class': some_class, 'teach': teach}
    except Classes.DoesNotExist:
        raise Http404("Class does not exist")
    except Teach.DoesNotExist:
        raise Http404("Teach entry does not exist")
    return render(request, 'takai/session.html', context)

# Profile page
def profile(request, sid):
    try:
        some_ta = Students.objects.get(pk=sid)
    except Students.DoesNotExist:
        raise Http404("Student does not exist")
    return render(request, 'takai/profile.html', {'some_ta': some_ta})

# Search page
def search(request):
    return render(request, 'takai/search.html')


#response = "You're looking at the %s."
#return HttpResponse(response % id)
