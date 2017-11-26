# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse

from .. models import *
import datetime
from django.utils import timezone


def get_course_analytics(request):
    time_per_course = 0.0
    cumulative_time_courses = 0.0
    courses = Course.objects.filter(user=request.user)
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
        cumulative_time_courses += time_per_course
        
    context['time_taken_by_courses'] = cumulative_time_courses

    return JsonResponse(context)


def get_research_analytics(request):
    total_time_for_research = 0.0
    context = {}
    research_work = Research.objects.filter(user=request.user)

    for research in research_work:
        total_time_for_research += research.task_info.time_spent/3600.0

    print total_time_for_research
    context['time_taken_by_research'] = total_time_for_research
    return JsonResponse(context)


def get_misc_analytics(request):
    total_time_for_misc = 0.0
    context = {}
    misc_work = Misc.objects.filter(user=request.user)

    for misc in misc_work:
        total_time_for_misc += misc.task_info.time_spent/3600.0

    print total_time_for_misc
    context['time_taken_by_misc'] = total_time_for_misc
    return JsonResponse(context)


def get_tree_analytics(request):
    courses = Course.objects.filter(user=request.user)
    context = dict()
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


def grace_days(request):
    context = {}
    courses = Course.objects.filter(user=request.user)
    research_work = Research.objects.filter(user=request.user)
    context['research'] = []

    for course in courses:
        context[course.course_name] = []

    for research in research_work:
        if research.task_info.status == 2:
            expected_finish_datetime = datetime.datetime.combine(research.task_info.expected_finish_date, research.task_info.expected_finish_time)
            if research.task_info.stop_time > expected_finish_datetime:
                context['research'].append({'time_exceeded_tasks':{'research_id': research.id, 'research_topic': research.topic}})
            else:
                context['research'].append({'on_time_tasks':{'research_id': research.id, 'research_topic': research.topic}})
    for course in courses:
        course_tasks = CourseTask.objects.filter(course=course)
        for course_task in course_tasks: 
            if course_task.task_info.status == 2:
                expected_finish_datetime = datetime.datetime.combine(course_task.task_info.expected_finish_date, course_task.task_info.expected_finish_time)
                if course_task.task_info.stop_time > expected_finish_datetime:
                    context[course.course_name].append({'time_exceeded_tasks':{'task_id': course_task.id, 'task_name': course_task.name}})
                else:
                    context[course.course_name].append({'on_time_tasks':{'task_id': course_task.id, 'task_name': course_task.name}})

    return JsonResponse(context)


def single_task_taken(request):
    context = {}
    courses = Course.objects.filter(user=request.user)
    research_work = Research.objects.filter(user=request.user)
    context['research'] = []

    for course in courses:
        context[course.course_name] = []
        course_tasks = CourseTask.objects.filter(course=course)
        for course_task in course_tasks:
            context[course.course_name].append({'task_id': course_task.id, 'task_name': course_task.name,
                                                'time_taken': course_task.task_info.time_spent})

    for research in research_work:
        context['research'].append({'topic': research.topic, 'time_taken': research.task_info.time_spent})

    return JsonResponse(context)
                



