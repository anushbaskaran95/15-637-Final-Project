# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse

from .. models import *
import datetime
from django.utils import timezone


def get_course_analytics(request):
    time_per_course = 0.0
    cummulative_time_courses = 0.0
    courses = Course.objects.all()
    context = {}

    for course in courses:
        course_tasks = CourseTask.objects.filter(course=course)
        for course_task in course_tasks:
            time_per_course += course_task.task_info.time_spent/3600.0
            print course.course_name
            print course_task.name
            print time_per_course 
            print "-------------"

        context[course.course_name] = time_per_course
        cummulative_time_courses += time_per_course
        
    context['time_taken_by_courses'] = cummulative_time_courses

    return JsonResponse(context)

def get_research_analytics(request):
    total_time_for_research = 0.0
    context = {}
    research_work = Research.objects.all()

    for research in research_work:
        total_time_for_research += research.task_info.time_spent/3600.0

    print total_time_for_research
    context['time_taken_by_research'] = total_time_for_research
    return JsonResponse(context)

def get_misc_analytics(request):
    total_time_for_misc = 0.0
    misc_work = Misc.objects.all()

    for misc in misc_work:
        total_time_for_misc += misc.task_info.time_spent/3600.0

    print total_time_for_misc
    return HttpResponse('')

def get_tree_analytics(request):
    username = request.user.username
    courses = Course.objects.all()
    context = {}
    context['name'] = request.user.username
    context['children'] = []
    index = 0

    for course in courses:
        course_name = course.course_name
        context['children'].append({'name': course_name, 'children': []})
        
    while index <= (len(context['children']) - 1):
        for course in courses:
            course_tasks = CourseTask.objects.filter(course=course)
            for course_task in course_tasks: 
                if course_task.task_info.status == 0:
                    context['children'][index]['children'].append({'name': course_task.name, 'status': 'ongoing'})
                elif course_task.task_info.status == 1:
                    context['children'][index]['children'].append({'name': course_task.name, 'status': 'paused'})
                elif course_task.task_info.status == 2:
                    context['children'][index]['children'].append({'name': course_task.name, 'status': 'stopped'})

            index = index + 1
            if index == len(courses):
                break
            
            
    return JsonResponse(context)