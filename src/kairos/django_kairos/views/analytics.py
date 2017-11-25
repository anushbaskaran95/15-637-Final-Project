# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404

from .. models import *
import datetime
from django.utils import timezone


def get_course_analytics(request):
    time_per_course = 0.0
    courses = Course.objects.all()

    for course in courses:
        course_tasks = CourseTask.objects.filter(course=course)
        for course_task in course_tasks:
            time_per_course += course_task.task_info.time_spent

    return HttpResponse('')
