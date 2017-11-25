# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404

from .. models import *
import datetime
from django.utils import timezone


def get_course_analytics(request):
    time_per_course = 0.0
    cummulative_time_courses = 0.0
    courses = Course.objects.all()

    for course in courses:
        course_tasks = CourseTask.objects.filter(course=course)
        for course_task in course_tasks:
            time_per_course += course_task.task_info.time_spent/3600.0
            print course.course_name
            print course_task.name
            print time_per_course 
            print "-------------"

        cummulative_time_courses += time_per_course
        
    print cummulative_time_courses

    return HttpResponse('')

def get_research_analytics(request):
    total_time_for_research = 0.0
    research_work = Research.objects.all()

    for research in research_work:
        total_time_for_research += research.task_info.time_spent/3600.0

    print total_time_for_research
    return HttpResponse('')