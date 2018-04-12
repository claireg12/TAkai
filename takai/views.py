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

from .models import Classes, Students, Enroll, Session, Mentor, Teach, Professors, Host, Ta
import pdb

def isProfessor(request):
    return request.user.groups.filter(name='Professors').exists()

def getUserId(request):
    if isProfessor(request):
        user_id = Professors.objects.get(email=request.user.email).fid
    else:
        user_id = Students.objects.get(email=request.user.email).sid
    return user_id


# Home page
@login_required
def semester(request, year, semester):

    # TODO: need to exclude my_classes from all_classes
    #       (.exclude() doesnt' work (yet) my_classes is from Teach and all_classes is from Enroll)
    all_classes = Session.objects.filter(semester=semester, year=year)

    if isProfessor(request):
        my_classes = Teach.objects.filter(session__semester=semester, session__year=year, professor__fid=getUserId(request))
        context = {'all_classes': all_classes, 'my_classes':my_classes, 'year': year, 'semester':semester, 'user_id' : getUserId(request)}
        return render(request, 'takai/semester_prof.html', context)
    else:
        my_classes = Enroll.objects.filter(session__semester=semester, session__year=year, student__sid=getUserId(request))
        context = {'all_classes': all_classes, 'my_classes':my_classes, 'year': year, 'semester':semester, 'user_id' : getUserId(request)}
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
    if request.user.groups.filter(name='Professors').exists():
        return render(request, 'takai/session_prof.html', context)
    else:
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


@login_required
def teach(request, year, semester, cid):
    prof = Professors.objects.get(fid=getUserId(request))
    session = Session.objects.get(theclass=cid)

    if (Teach.objects.filter(professor=prof, session=session)):
        all_classes = Session.objects.filter(semester=semester, year=year)
        context = {'all_classes': all_classes, 'year': year, 'semester':semester, 'user_id' : prof.fid}
        return render(request, 'takai/semester.html', context)
    else:
        teaching = Teach.objects.create(professor = prof, session=session,)
        teaching.save()
        return HttpResponseRedirect(reverse('semester', args = (year,semester)))

@login_required
def enroll(request, year, semester, cid):
    student = Students.objects.get(sid=getUserId(request))
    session = Session.objects.get(theclass=cid)

    if (Enroll.objects.filter(student=student, session=session)):
        all_classes = Session.objects.filter(semester=semester, year=year)
        context = {'all_classes': all_classes, 'year': year, 'semester':semester, 'user_id' : student.sid}
        return render(request, 'takai/semester.html', context)
    else:
        enrollment = Enroll.objects.create(student = student, session=session,)
        enrollment.save()
        return HttpResponseRedirect(reverse('semester', args = (year,semester)))

    return HttpResponseRedirect(reverse('semester', args = (year,semester)))

# How a prof assigns a TA to a class
# If the student is not a TA yet, adds it as a TA and as a mentor for that class
def prof(request, year, semester, cid):
    student = Students.objects.get(name=request.POST.get('student_name_field', False))
    session = Session.objects.get(theclass=cid)
    try:
        returned_student_name = student.name
    except (KeyError, Students.DoesNotExist):
        return render(request, 'takai/semester_prof.html',{
        'student name': returned_student_name,
        'error message': "This student does not exist",
        })
    else:
        if not Ta.objects.filter(student=student):
            assignment1 = Ta.objects.create(student = student,)
            assignment1.save()
        ta = Ta.objects.get(student=student)
        assignment2 = Mentor.objects.create(student = ta, session=session,)
        assignment2.save()

    return HttpResponseRedirect(reverse('semester', args = (year,semester)))
