# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Course)
admin.site.register(TaskInfo)
admin.site.register(CourseTask)
admin.site.register(Research)
admin.site.register(Misc)