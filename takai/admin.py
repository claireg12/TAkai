# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Classes, Session, Students, Enroll, Mentor, Mentorsessions, Professors, Ta

admin.site.register(Classes)
admin.site.register(Session)
admin.site.register(Students)
#admin.site.register(Enroll)
@admin.register(Enroll)
class EnrollAdmin(admin.ModelAdmin):
	list_display = ('student','session')
	search_fields = ('student',)

admin.site.register(Mentor)
admin.site.register(Mentorsessions)
admin.site.register(Professors)
admin.site.register(Ta)