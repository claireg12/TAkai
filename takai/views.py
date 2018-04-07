# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.models import Permission, User
from django.contrib.auth import authenticate, login



from .models import Classes, Students



# Home page
@login_required
def semester(request, year, semester):
    ordered_classes = Classes.objects.order_by('cid')
    current_classes = ordered_classes.filter(session__semester=semester, session__year=year)
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
    except Classes.DoesNotExist:
        raise Http404("Class does not exist")
    return render(request, 'takai/session.html', {'some_class': some_class})

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



#response = "You're looking at the %s."
#return HttpResponse(response % id)
