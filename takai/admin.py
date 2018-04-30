# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Classes, Session, Students, Enroll, Mentor, Mentorsessions, Professors, Ta, Teach, Host, Application, Classinterest, Interestcode, Availability, Availabilitycode

admin.site.register(Classes)
admin.site.register(Session)
admin.site.register(Students)
admin.site.register(Teach)
admin.site.register(Host)
@admin.register(Enroll)
class EnrollAdmin(admin.ModelAdmin):
	list_display = ('student','session')
	search_fields = ('student',)

admin.site.register(Mentor)
admin.site.register(Mentorsessions)
admin.site.register(Professors)
admin.site.register(Ta)
admin.site.register(Application)
admin.site.register(Classinterest)
admin.site.register(Interestcode)
admin.site.register(Availability)
admin.site.register(Availabilitycode)
