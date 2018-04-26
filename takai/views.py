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
from django.contrib import messages

from .models import Classes, Students, Enroll, Session, Mentor, Teach, Professors, Host,Ta#,Application, Classinterest, Interestcode
from .forms import *
from django.forms import ModelForm, modelformset_factory

import pdb

def isProfessor(user):
    return user.groups.filter(name='Professors').exists()

def getUserId(request):
    if isProfessor(request.user):
        user_id = Professors.objects.get(email=request.user.email).fid
    else:
        user_id = Students.objects.get(email=request.user.email).sid
    return user_id

def isTA(pk):
    try:
        ta = Ta.objects.get(pk=pk)
        return True
    except User.DoesNotExist:
        return False

# Home page
@login_required
def semester(request, year, semester):

    all_classes = Session.objects.filter(semester=semester, year=year)

    if isProfessor(request.user):
        my_classes = Session.objects.filter(teach__professor__fid=getUserId(request), semester=semester, year=year)
        other_classes = set(all_classes).difference(set(my_classes))
        context = {'my_classes':my_classes, 'year': year, 'semester':semester, 'user_id' : getUserId(request), 'other_classes':other_classes, 'name':request.user.first_name}
        return render(request, 'takai/semester_prof.html', context)
    else:
        my_classes = Session.objects.filter(enroll__student__sid=getUserId(request), semester=semester, year=year)
        other_classes = set(all_classes).difference(set(my_classes))
        context = {'my_classes':my_classes, 'year': year, 'semester':semester, 'user_id' : getUserId(request), 'other_classes':other_classes, 'name':request.user.first_name}
        return render(request, 'takai/semester.html', context)

# Class page
@login_required
def session(request, year, semester, cid):
    try:
        some_class = Classes.objects.get(pk=cid)
        some_session = Session.objects.get(theclass=cid)
        tas = Mentor.objects.filter(session__theclass = some_class, session__semester = semester, session__year = year)
        profs = Teach.objects.filter(session__theclass = some_class, session__semester = semester, session__year = year)
        mentorsessions = Host.objects.filter(session__theclass = some_class, session__semester = semester, session__year = year)

        context = {'some_session': some_session, 'some_class': some_class,'year': year, 'semester': semester, 'tas': tas, 'profs': profs, 'mentorsessions': mentorsessions, 'name':request.user.first_name} # removed teach
    except Classes.DoesNotExist:
        raise Http404("Class does not exist")
    # except Teach.DoesNotExist:
    #     raise Http404("Teach entry does not exist")
    if request.user.groups.filter(name='Professors').exists():
        return render(request, 'takai/session_prof.html', context)
    else:
        return render(request, 'takai/session.html', context)

# TODO: why doesn't this permission work?
# @user_passes_test(isProfessor)

class UpdateSession(UpdateView):
    model = Session
    template_name_suffix = '_edit_prof'
    form_class = UpdateSessionInfo
    second_form_class = UpdateProfessorInfo

    def get_success_url(self):
        session_id = self.kwargs['pk']
        some_session = Session.objects.get(pk=session_id)
        return reverse_lazy('session', args = (some_session.year,some_session.semester,some_session.theclass.cid))

    def get_context_data(self, **kwargs):
        context = super(UpdateSession, self).get_context_data(**kwargs)
        session_id = self.kwargs['pk']
        teaches = Teach.objects.get(session=session_id)
        some_professor = teaches.professor
        context['Professors'] = Professors.objects.get(fid=teaches.professor.fid)
        context['prof_form'] = self.second_form_class(instance=some_professor)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Save the changes to the professor table
        # Changes to the session table are automatically saved
        if 'email' in request.POST:
            professor_update_form = self.second_form_class(request.POST)
            if professor_update_form.is_valid():
                professor_update = professor_update_form.cleaned_data
                some_professor = Professors(**professor_update)

                teaches = Teach.objects.get(session=self.kwargs['pk'])
                class_professor = Professors.objects.get(fid = teaches.professor.fid)
                some_professor.fid = class_professor.fid
                some_professor.save()
                return super(UpdateSession, self).post(request, *args, **kwargs)
            else:
                return super(UpdateSession, self).post(request, *args, **kwargs)
        else:
            return super(UpdateSession, self).post(request, *args, **kwargs)

class UpdateMentorSession(UpdateView):
    model = Mentorsessions
    template_name_suffix = '_edit'
    form_class = UpdateMSInfo

    def get_success_url(self):
        return reverse_lazy('session', args = (self.kwargs['year'],self.kwargs['semester'],self.kwargs['cid']))

#not really working
class UpdateTa(UpdateView):
    model = Ta
    template_name_suffix = '_edit'
    form_class = UpdateTaInfo

    def get_context_data(self, **kwargs):
        context = super(UpdateTa, self).get_context_data(**kwargs)
        #pdb.set_trace()

        if isTA(self.kwargs['pk']):
            return context
        else:
            raise Http404("You need TA permissions to edit this")

    def get_success_url(self):
        return reverse_lazy('session', args = (self.kwargs['year'],self.kwargs['semester'],self.kwargs['cid']))

def TaApplication(request): #or class (CreateView)
    #model = Classes
    #template_name_suffix = '_apply' #is it being used?
    ApplicationFormSet = modelformset_factory(Application, fields=('student', 'school', 'major', 'qualities', 'num_hours_week', 'lab_availability'))
    ClassinterestFormSet = modelformset_factory(Classinterest, fields=('student', 'session', 'interestcode'))
    if request.method == 'POST':
        formset1 = ApplicationFormSet(
        request.POST, request.FILES,
        queryset=Application.objects.all(), # change to none? not sure
        )
        formset2 = ClassinterestFormSet(
        request.POST, request.FILES,
        queryset=Classinterest.objects.all(), # change to none? not sure
        )
        if formset1.is_valid():
            formset1.save()
        if formset2.is_valid():
            formset2.save()
    else:
        formset1 = ApplicationFormSet(queryset=Application.objects.none())
        formset2 = ClassinterestFormSet(queryset=Classinterest.objects.none())


    return render(request, 'takai/apply.html', {'name':request.user.first_name, 'formset1': formset1, 'formset2': formset2})
    # how to redirect to the semester page??

# Profile page
@login_required
# TODO: this should redirect to session page (ie just stay on same page), instead of redirecting to semester page, which is default
@user_passes_test(isProfessor)
# @permission_required('professors.can_add_professors', raise_exception=True)
def profile(request, sid):
    try:
        some_ta = Students.objects.get(pk=sid)
    except Students.DoesNotExist:
        raise Http404("Student does not exist")
    return render(request, 'takai/profile.html', {'some_ta': some_ta, 'name':request.user.first_name})

# Search page
@login_required
# TODO: this should redirect to session page (ie just stay on same page), instead of redirecting to semester page, which is default
@user_passes_test(isProfessor)
#@permission_required('professors.can_add_professors', raise_exception=True)
def search(request):
        return render(request, 'takai/search.html', {'name':request.user.first_name})


# When a professor wants to teach a course
@login_required
def teach(request, year, semester, cid):
    prof = Professors.objects.get(fid=getUserId(request))
    session = Session.objects.get(theclass=cid)

    # if (Teach.objects.filter(professor=prof, session=session)):
    #     all_classes = Session.objects.filter(semester=semester, year=year)
    #     my_classes = Teach.objects.filter(session__semester=semester, session__year=year, professor__fid=getUserId(request))
    #     context = {'all_classes': all_classes, year: year, 'semester':semester, 'user_id' : prof.fid}
    #     return render(request, 'takai/semester_prof.html', context)
    # else:

    teaching = Teach.objects.create(professor = prof, session=session,)
    teaching.save()
    return HttpResponseRedirect(reverse('semester', args = (year,semester)))

# When a student wants to enroll in a course
@login_required
def enroll(request, year, semester, cid):
    student = Students.objects.get(sid=getUserId(request))
    session = Session.objects.get(theclass=cid)

    # if (Enroll.objects.filter(student=student, session=session)):
    #     all_classes = Session.objects.filter(semester=semester, year=year)
    #     my_classes = Teach.objects.filter(session__semester=semester, session__year=year, professor__fid=getUserId(request))
    #     context = {'all_classes': all_classes,'year': year, 'semester':semester, 'user_id' : student.sid}
    #     return render(request, 'takai/semester.html', context)
    # else:
    enrollment = Enroll.objects.create(student = student, session=session,)
    enrollment.save()
    return HttpResponseRedirect(reverse('semester', args = (year,semester)))

    # return HttpResponseRedirect(reverse('semester', args = (year,semester)))

# How a prof assigns a TA to a class
# If the student is not a TA yet, adds it as a TA and as a mentor for that class
@login_required
def prof(request, year, semester, cid):

    session1 = Session.objects.get(theclass=cid)

    try:
        student = Students.objects.get(name=request.POST.get('student_name_field', False))
        returned_student_name = student.name
    except (KeyError, Students.DoesNotExist):
        return session(request, year, semester, cid)
    else:
        if not Ta.objects.filter(student=student):
            assignment1 = Ta.objects.create(student = student,)
            assignment1.save()
        ta = Ta.objects.get(student=student)
        assignment2 = Mentor.objects.create(ta = ta, session=session1,)
        assignment2.save()

    return session(request, year, semester, cid)
