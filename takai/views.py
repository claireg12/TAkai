# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.urls import reverse

import pdb

from .models import Classes, Students, Enroll, Session

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
    except Classes.DoesNotExist:
        raise Http404("Class does not exist")
    return render(request, 'takai/session.html', {'some_class': some_class, 'year': year, 'semester': semester})

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

def enroll(request, year, semester, cid):
    #student = get_object_or_404(Students, pk=request.POST['student_id_field'])
    #session = get_object_or_404(Session, pk=cid)
    student = Students.objects.get(pk=request.POST['student_id_field'])
    session = Session.objects.get(pk=cid)
    #pdb.set_trace()
    try: 
        returned_student_id = student.sid
    except (KeyError,Students.DoesNotExist):
        return render(request, 'takai/semester.html',{
        'student id': returned_student_id,
        'error message': "This is not a valid student id.",
            })
    else:
        enrollment = Enroll.objects.create(student = student, session=session,)
        #pdb.set_trace()
        enrollment.save()
    


    return HttpResponseRedirect(reverse('semester', args = (year,semester)))


# Enroll.objects.create



#response = "You're looking at the %s."
#return HttpResponse(response % id)
