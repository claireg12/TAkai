# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Classes, Session, Students

admin.site.register(Classes)
admin.site.register(Session)
admin.site.register(Students)


# Register your models here.
