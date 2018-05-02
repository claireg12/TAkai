# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.models import Permission, User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Q
from django.views.generic.edit import FormMixin
from django.db.models.query import QuerySet

from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm


from .models import Classes, Students, Enroll, Session, Mentor, Teach, Professors, Host,Ta,Application, Classinterest, Interestcode, Availability, Availabilitycode
from .forms import *
from django.forms import ModelForm, modelformset_factory, formset_factory

import pdb

current_semester = "Spring"
current_year = "2018"

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
        mentor_classes = Session.objects.filter(mentor__ta__student__sid=getUserId(request), semester=semester, year=year)
        other_classes = set(other_classes).difference(set(mentor_classes))
        my_classes = set(my_classes).difference(set(mentor_classes))
        context = {'my_classes':my_classes, 'year': year, 'semester':semester, 'user_id' : getUserId(request), 'other_classes':other_classes, 'name':request.user.first_name, 'mentor_classes':mentor_classes}
        return render(request, 'takai/semester.html', context)

# Class page
@login_required
def session(request, year, semester, cid):
    try:
        some_class = Classes.objects.get(pk=cid)
        some_session = Session.objects.get(theclass=cid, semester=semester, year=year)
        mentors = Mentor.objects.filter(session__theclass = some_class, session__semester = semester, session__year = year)
        profs = Teach.objects.filter(session__theclass = some_class, session__semester = semester, session__year = year)
        #get tas to filter host objects
        tas = Mentor.objects.filter(session__theclass = some_class, session__semester = semester, session__year = year).values_list('ta', flat = True)
        mentorsessions = Host.objects.filter(session__theclass = some_class, session__semester = semester, session__year = year, ta__in = tas)

        context = {'some_session': some_session, 'some_class': some_class,'year': year, 'semester': semester, 'tas': mentors, 'profs': profs, 'mentorsessions': mentorsessions, 'name':request.user.first_name} # removed teach
    except Classes.DoesNotExist:
        raise Http404("Class does not exist")
    if request.user.groups.filter(name='Professors').exists():
        return render(request, 'takai/session_prof.html', context)
    else:
        return render(request, 'takai/session.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate user and login
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            # Add to Students table
            grad_year = form.cleaned_data.get('graduation_year')
            id_num = form.cleaned_data.get('id_number')
            full_name = user.first_name + ' ' + user.last_name
            student = Students.objects.create(sid = id_num, name=full_name, gradyear=grad_year, email=user.email)
            student.save()
            # Redirect to homepage for current semester
            return HttpResponseRedirect(reverse('semester', args = (current_year,current_semester)))
    else:
        form = SignUpForm()
    return render(request, 'takai/signup.html', {'form': form})

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
        try:
            teaches = Teach.objects.get(session=session_id)
            some_professor = teaches.professor
            context['Professors'] = Professors.objects.get(fid=teaches.professor.fid)
            context['prof_form'] = self.second_form_class(instance=some_professor)
        except Teach.DoesNotExist:
            teaches = set()
            context['Professors'] = set()
            context['prof_form'] = set()
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

def addMentorSession(request, year, semester,cid, session):
    if request.method == 'POST':
        form = AddMSInfo(request.POST)
        if form.is_valid():
            session = Session.objects.get(pk = session)
            # Authenticate user and login
            day = form.cleaned_data.get('day')
            time = form.cleaned_data.get('time')
            location = form.cleaned_data.get('location')
            mentorsession = Mentorsessions.objects.create(session = session, time = time, day = day, location = location)
            mentorsession.save()

            userEmail = request.user.email
            student = Students.objects.get(email = userEmail)
            ta = Ta.objects.get(student = student)
            host = Host.objects.create(ta= ta, session = session, mentorsesh = mentorsession)
            host.save()
            # Redirect to homepage for current semester
            return HttpResponseRedirect(reverse('session', args = (year,semester,cid)))
    else:
        form = AddMSInfo()

    return render(request, 'takai/mentorsessions_add.html', {'form': form})

def UpdateTa(request, year, semester,cid, pk):
    if request.method == 'POST':
        form = UpdateTaInfo(request.POST)
        if form.is_valid():
            student = Students.objects.get(email=request.user.email)
            bio = form.cleaned_data.get('bio')
            ta = Ta.objects.get(student=student)
            ta.bio = bio
            ta.save()
            return HttpResponseRedirect(reverse('session', args = (current_year,current_semester,cid)))
    else:
        form = UpdateTaInfo()
    return render(request, 'takai/ta_edit.html', {'form': form})

class DeleteTa(DeleteView):
    model = Mentor

    def get_success_url(self):
        return reverse_lazy('session', args = (self.kwargs['year'],self.kwargs['semester'],self.kwargs['cid']))

def TaApplication(request, year, semester):
    if semester == "Fall":
        next_semester = "Spring"
        next_year = year + 1
    else:
        next_semester = "Fall"
        next_year = year

    all_classes = Session.objects.filter(semester=next_semester, year=next_year)
    num_classes = Session.objects.filter(semester=next_semester, year=next_year).count()
    student = Students.objects.get(email=request.user.email)

    ClassinterestFormSet = formset_factory(ClassInterestForm, extra=num_classes, formset=BaseArticleFormSet)

    if request.method == 'POST':
        appForm = ApplicationForm(request.POST)
        if appForm.is_valid():
            application = appForm.cleaned_data
            application['student_id'] = getUserId(request)
            application['semester'] = next_semester
            application['year'] = next_year

            formset2 = ClassinterestFormSet(
            request.POST, request.FILES, initial=[{'student':student,}]
            )

            student = Students.objects.get(sid = getUserId(request))
            availability_list = request.POST.getlist('availabilitycode')

            if formset2.is_valid():
                new_application = Application.objects.create(**application)
                new_application.save()

                for availability in availability_list:
                    availabilitycode = Availabilitycode.objects.get(code=availability)
                    new_availability = Availability.objects.create(availabilitycode = availabilitycode, student = student)
                    new_availability.save()

                for form in formset2:
                    clean_form = form.cleaned_data
                    clean_form['student_id'] = getUserId(request)
                    new_application = Classinterest.objects.create(**clean_form)
                    new_application.save()
            else:
                availabilityForm = AvailabilityForm()
                context = {'all_classes':all_classes, 'cur_year':year, 'cur_semester':semester, 'next_year': next_year, 'next_semester': next_semester,'name':request.user.first_name, 'formset1': appForm, 'formset2': formset2,'formset3': availabilityForm}
                return render(request, 'takai/apply.html', context)

            return HttpResponseRedirect(reverse('semester', args = (year,semester)))
    else:
        appForm = ApplicationForm()
        classInterestForm = ClassinterestFormSet()
        for form in classInterestForm:
            form.fields["session"].queryset = all_classes
        availabilityForm = AvailabilityForm()
        context = {'all_classes':all_classes, 'cur_year':year, 'cur_semester':semester, 'next_year': next_year, 'next_semester': next_semester,'name':request.user.first_name, 'formset1': appForm, 'formset2': classInterestForm,'formset3': availabilityForm}
        return render(request, 'takai/apply.html', context)

# Profile page
@login_required
@user_passes_test(isProfessor)
def profile(request, sid):
    try:
        some_ta = Students.objects.get(pk=sid)
        ta_apps = Application.objects.filter(student=sid)
        ta_avails = Availability.objects.filter(student=sid)
        ta_interests = Classinterest.objects.filter(student=sid)
    except Students.DoesNotExist:
        raise Http404("Student does not exist")
    return render(request, 'takai/profile.html', {'some_ta': some_ta, 'apps': ta_apps, 'avails': ta_avails, 'interests':ta_interests, 'name':request.user.first_name, 'semester':current_semester, 'year':current_year})

# Search page
@user_passes_test(isProfessor)
def adv_search(request, year, semester):
    sessions = Session.objects.all()
    interests = Interestcode.objects.all()
    availabilities = Availabilitycode.objects.all()
    context = {'year': year, 'semester':semester, 'sessions': sessions, 'interests':interests, 'availabilities': availabilities, 'user_id' : getUserId(request), 'name':request.user.first_name}
    try:
        if request.method == 'POST':
            session = request.POST.get('session', False)
            interest = request.POST.get('interest', False)
            availability = request.POST.get('availability', False)
            if availability == "anyavail":
                results1 = Availability.objects.all().values_list('student', flat="True")
            else:
                results1 = Availability.objects.filter(availabilitycode=availability).values_list('student', flat="True")
            if interest == "anyinterest":
                results2 = Classinterest.objects.all().values_list('student', flat="True")
            else:
                results2 = Classinterest.objects.filter(session=session, interestcode=interest).values_list('student', flat="True")
            results = set(results1).intersection(set(results2))
            students = []
            for result in results:
                students.append(Students.objects.filter(sid=result))
            return render(request, 'takai/searchresults.html', {'name':request.user.first_name, 'results':students, 'semester':current_semester, 'year':current_year})
    except:
        raise Http404("Invalid Search")
    return render(request, 'takai/adv_search.html', context)

# When a professor wants to teach a course
@login_required
def teach(request, year, semester, cid):
    prof = Professors.objects.get(fid=getUserId(request))
    session = Session.objects.get(theclass=cid, semester=semester, year=year)
    teaching = Teach.objects.create(professor = prof, session=session,)
    teaching.save()
    return HttpResponseRedirect(reverse('semester', args = (year,semester)))

# When a professor wants to unteach a course
@login_required
def unteach(request, year, semester, cid):
    prof = Professors.objects.get(fid=getUserId(request))
    session = Session.objects.get(theclass=cid, semester=semester, year=year)
    unteach = Teach.objects.filter(professor = prof, session=session,)
    unteach.delete()
    return HttpResponseRedirect(reverse('semester', args = (year,semester)))

# When a student wants to enroll in a course
@login_required
def enroll(request, year, semester, cid):
    student = Students.objects.get(sid=getUserId(request))
    session = Session.objects.get(theclass=cid, semester=semester, year=year)
    enrollment = Enroll.objects.create(student = student, session=session,)
    enrollment.save()
    return HttpResponseRedirect(reverse('semester', args = (year,semester)))

# When a student wants to unenroll in a course
@login_required
def unenroll(request, year, semester, cid):
    student = Students.objects.get(sid=getUserId(request))
    session = Session.objects.get(theclass=cid, semester=semester, year=year)
    unenrollment = Enroll.objects.filter(student = student, session=session,)
    unenrollment.delete()
    return HttpResponseRedirect(reverse('semester', args = (year,semester)))

# How a prof assigns a TA to a class
# If the student is not a TA yet, adds it as a TA and as a mentor for that class
@login_required
def prof(request, year, semester, cid):
    session1 = Session.objects.get(theclass=cid, semester=semester, year=year)
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
