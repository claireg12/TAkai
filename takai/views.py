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
        # we're getting the student/professor object based on the email, but since it's not
        # required to be unique, you could have two users with same email, which would throw
        # an error
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
        # other_classes = set(o_classes).difference(set(mentor_classes))

        context = {'my_classes':my_classes, 'year': year, 'semester':semester, 'user_id' : getUserId(request), 'other_classes':other_classes, 'name':request.user.first_name, 'mentor_classes':mentor_classes}
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

#not really working
class UpdateTa(UpdateView):
    model = Ta
    template_name_suffix = '_edit'
    form_class = UpdateTaInfo #initial={'student': 10314767}

    def get_context_data(self, **kwargs):
        context = super(UpdateTa, self).get_context_data(**kwargs)
        #pdb.set_trace()

        if isTA(self.kwargs['pk']):
            return context
        else:
            raise Http404("You need TA permissions to edit this")

    # def get_initial(self):
    #     return { 'student': self.kwargs['pk']}

    def get_success_url(self):
        return reverse_lazy('session', args = (self.kwargs['year'],self.kwargs['semester'],self.kwargs['cid']))

class DeleteTa(DeleteView):
    model = Mentor

    def get_success_url(self):
        return reverse_lazy('session', args = (self.kwargs['year'],self.kwargs['semester'],self.kwargs['cid']))

def TaApplication(request, year, semester): #or class (CreateView)
    all_classes = Session.objects.filter(semester=semester, year=year)
    num_classes = Session.objects.count() # filter by semester
    classes = Session.objects.all() # filter by semester

    ClassinterestFormSet = formset_factory(ClassInterestForm, extra=num_classes)

    if request.method == 'POST':
        appForm = ApplicationForm(request.POST)
        if appForm.is_valid():
            application = appForm.cleaned_data
            application['student_id'] = getUserId(request)
            if semester == "Fall":
                application['semester'] = "Spring"
                application['year'] = year + 1
            else:
                application['semester'] = "Fall"
                application['year'] = year
            new_application = Application.objects.create(**application)
            new_application.save()
        formset2 = ClassinterestFormSet(
        request.POST, request.FILES,)

        # save the availabilty information
        student = Students.objects.get(sid = getUserId(request))
        availability_list = request.POST.getlist('availabilitycode')
        for availability in availability_list:
            availabilitycode = Availabilitycode.objects.get(code=availability)
            new_availability = Availability.objects.create(availabilitycode = availabilitycode, student = student)

        if formset2.is_valid():
            formset2.save()

        return HttpResponseRedirect(reverse('semester', args = (year,semester)))

    else:
        initial2 = []
        for sesh in classes:
            initial2.append({'sesh': sesh})
        appForm = ApplicationForm()
        classInterestForm = ClassinterestFormSet()
        # classInterestForm = ClassinterestFormSet(initial=[{'sesh': sesh} for sesh in classes])
        availabilityForm = AvailabilityForm()
        context = {'all_classes':all_classes, 'year': year, 'semester':semester,'name':request.user.first_name, 'formset1': appForm, 'formset2': classInterestForm,'formset3': availabilityForm}
        return render(request, 'takai/apply.html', context)
    # how to redirect to the semester page??

# Profile page
@login_required
# TODO: this should redirect to session page (ie just stay on same page), instead of redirecting to semester page, which is default
@user_passes_test(isProfessor)
def profile(request, sid):
    try:
        some_ta = Students.objects.get(pk=sid)
        ta_apps = Application.objects.filter(student=sid)
        ta_avails = Availability.objects.filter(student=sid)
        ta_interests = Classinterest.objects.filter(student=sid)
    except Students.DoesNotExist:
        raise Http404("Student does not exist")
    return render(request, 'takai/profile.html', {'some_ta': some_ta, 'apps': ta_apps, 'avails': ta_avails, 'interests':ta_interests, 'name':request.user.first_name})

# Search page
@user_passes_test(isProfessor)
def adv_search(request, year, semester):
    sessions = Session.objects.filter(semester=semester, year=year)
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
            names = []
            sids = []
            students = []
            for result in results:
                names.append(Students.objects.filter(sid=result).values_list('name')[0])
                sids.append(Students.objects.filter(sid=result).values_list('sid')[0])
                students.append(Students.objects.filter(sid=result))
            allresults = zip(names, sids)
            return render(request, 'takai/searchresults.html', {'name':request.user.first_name, 'results':students})
    except:
        raise Http404("Invalid Search")

    return render(request, 'takai/adv_search.html', context)


# When a professor wants to teach a course
@login_required
def teach(request, year, semester, cid):
    prof = Professors.objects.get(fid=getUserId(request))
    session = Session.objects.get(theclass=cid)
    teaching = Teach.objects.create(professor = prof, session=session,)
    teaching.save()
    return HttpResponseRedirect(reverse('semester', args = (year,semester)))

# When a professor wants to unteach a course
@login_required
def unteach(request, year, semester, cid):
    prof = Professors.objects.get(fid=getUserId(request))
    session = Session.objects.get(theclass=cid)
    unteach = Teach.objects.filter(professor = prof, session=session,)
    unteach.delete()
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

# When a student wants to unenroll in a course
@login_required
def unenroll(request, year, semester, cid):
    student = Students.objects.get(sid=getUserId(request))
    session = Session.objects.get(theclass=cid)

    # if (Enroll.objects.filter(student=student, session=session)):
    #     all_classes = Session.objects.filter(semester=semester, year=year)
    #     my_classes = Teach.objects.filter(session__semester=semester, session__year=year, professor__fid=getUserId(request))
    #     context = {'all_classes': all_classes,'year': year, 'semester':semester, 'user_id' : student.sid}
    #     return render(request, 'takai/semester.html', context)
    # else:
    unenrollment = Enroll.objects.filter(student = student, session=session,)
    unenrollment.delete()
    return HttpResponseRedirect(reverse('semester', args = (year,semester)))

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

@login_required
class SearchView(generic.ListView):
    #template_name = 'polls/index.html'
    context_object_name = 'ta_searched_list'

    def get_queryset(self):
        return Ta.objects.all()
