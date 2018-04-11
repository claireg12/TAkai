# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.models import Permission, User
from django.contrib.auth import authenticate, login

from .models import Classes, Students, Enroll, Session, Mentor, Teach, Professors, Host
import pdb


# Home page
@login_required
def semester(request, year, semester):
    # ordered_classes = Classes.objects.order_by('cid')
    # current_classes = ordered_classes.filter(session__semester=semester, session__year=year)
    current_classes = Session.objects.filter(semester=semester, year=year)
    context = {'current_classes': current_classes, 'year': year, 'semester':semester}

    if request.user.has_perm('professors.can_add_professors'):
        return render(request, 'takai/semester_prof.html', context)
    else:
        return render(request, 'takai/semester.html', context)

# Class page
@login_required
def session(request, year, semester, cid):
    try:
        some_class = Classes.objects.get(pk=cid)
        tas = Mentor.objects.filter(session__theclass = some_class, session__semester = semester, session__year = year)
        profs = Teach.objects.filter(session__theclass = some_class, session__semester = semester, session__year = year)
        mentorsessions = Host.objects.filter(session__theclass = some_class, session__semester = semester, session__year = year)

        context = {'some_class': some_class,'year': year, 'semester': semester, 'tas': tas, 'profs': profs, 'mentorsessions': mentorsessions} # removed teach
    except Classes.DoesNotExist:
        raise Http404("Class does not exist")
    # except Teach.DoesNotExist:
    #     raise Http404("Teach entry does not exist")
    return render(request, 'takai/session.html', context)


# Profile page
@login_required
@permission_required('professors.can_add_professors', raise_exception=True)
def profile(request, sid):
    try:
        some_ta = Students.objects.get(pk=sid)
    except Students.DoesNotExist:
        raise Http404("Student does not exist")
    return render(request, 'takai/profile.html', {'some_ta': some_ta})

# Search page
@login_required
@permission_required('professors.can_add_professors', raise_exception=True)
def search(request):
        return render(request, 'takai/search.html')


def enroll(request, year, semester, cid):
    #student = get_object_or_404(Students, pk=request.POST['student_id_field'])
    #session = get_object_or_404(Session, pk=cid)
    student = Students.objects.get(pk=request.POST['student_id_field'])
    session = Session.objects.get(theclass=cid) # (pk=cid)
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
