# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from django.shortcuts import render

from .. models import *
import datetime
from django.utils import timezone


def analytics(request):
    return render(request, 'analytics/tree.html', context={'username': request.user.username})


def course_analytics(request):
    context = {'username': request.user.username}
    courses = Course.objects.filter(user=request.user)
    context['courses'] = courses
    return render(request, 'analytics/course_analytics.html', context)


def research_analytics(request):
    return render(request, 'analytics/research_analytics.html', context={'username': request.user.username})


def overall_analytics(request):
    return render(request, 'analytics/overall_analytics.html', context={'username': request.user.username})


def get_course_analytics(request):
    total_time_courses = 0.0
    courses = Course.objects.filter(user=request.user)
    context = {}
    now = timezone.now()
    context['time_per_course'] = []
    time_per_course_dict = {}
    for course in courses:
        time_per_course = 0.0
        course_tasks = CourseTask.objects.filter(course=course)
        context[course.course_name] = []

        for task in course_tasks:
            # time spent on paused or stopped task is set in DB
            if task.task_info.status == 1 or task.task_info.status == 2:
                time_spent = task.task_info.time_spent / 3600.0
            else:
                if task.task_info.time_spent is not None:
                    time_spent = ((now - task.task_info.continue_time).total_seconds() + task.task_info.time_spent) / 3600.0
                else:
                    time_spent = (now - task.task_info.continue_time).total_seconds() / 3600.0

            context[course.course_name].append({'course_id': course.id, 'task_name': task.name,
                                                'time_spent': time_spent, 'time_needed': task.task_info.time_needed})
            time_per_course += time_spent

        time_per_course_dict[course.course_name] = time_per_course
        total_time_courses += time_per_course
        
    context['total_time_courses'] = total_time_courses
    context['time_per_course'] = time_per_course_dict

    return JsonResponse(context)


def get_research_analytics(request):
    total_time_research = 0.0
    context = {}
    now = timezone.now()
    context['time_per_research'] = []
    time_per_research_dict = {}
    research_work = Research.objects.filter(user=request.user)

    for task in research_work:
        # time spent on paused or stopped task is set in DB
        if task.task_info.status == 1 or task.task_info.status == 2:
            time_spent = task.task_info.time_spent / 3600.0
        else:
            if task.task_info.time_spent is not None:
                time_spent = ((now - task.task_info.continue_time).total_seconds() + task.task_info.time_spent) / 3600.0
            else:
                time_spent = (now - task.task_info.continue_time).total_seconds() / 3600.0

        time_per_research_dict[task.topic] = time_spent
        total_time_research += time_spent

    context['total_time_research'] = total_time_research
    context['time_per_research'] = time_per_research_dict
    return JsonResponse(context)


def get_overall_analytics(request):
    total_time_misc = 0.0
    total_time_research = 0.0
    total_time_courses = 0.0
    context = {}
    now = timezone.now()
    misc_work = Misc.objects.filter(user=request.user)
    research_work = Research.objects.filter(user=request.user)
    courses = Course.objects.filter(user=request.user)

    for task in misc_work:
        # time spent on paused or stopped task is set in DB
        if task.task_info.status == 1 or task.task_info.status == 2:
            time_spent = task.task_info.time_spent / 3600.0
        else:
            if task.task_info.time_spent is not None:
                time_spent = ((now - task.task_info.continue_time).total_seconds() + task.task_info.time_spent) / 3600.0
            else:
                time_spent = (now - task.task_info.continue_time).total_seconds() / 3600.0

        total_time_misc += time_spent

    for task in research_work:
        # time spent on paused or stopped task is set in DB
        if task.task_info.status == 1 or task.task_info.status == 2:
            time_spent = task.task_info.time_spent / 3600.0
        else:
            if task.task_info.time_spent is not None:
                time_spent = ((now - task.task_info.continue_time).total_seconds() + task.task_info.time_spent) / 3600.0
            else:
                time_spent = (now - task.task_info.continue_time).total_seconds() / 3600.0

        total_time_research += time_spent

    for course in courses:
        course_tasks = CourseTask.objects.filter(course=course)
        for task in course_tasks:
            # time spent on paused or stopped task is set in DB
            if task.task_info.status == 1 or task.task_info.status == 2:
                time_spent = task.task_info.time_spent / 3600.0
            else:
                if task.task_info.time_spent is not None:
                    time_spent = ((
                                  now - task.task_info.continue_time).total_seconds() + task.task_info.time_spent) / 3600.0
                else:
                    time_spent = (now - task.task_info.continue_time).total_seconds() / 3600.0

            total_time_courses += time_spent

    context['total_time_courses'] = total_time_courses
    context['total_time_research'] = total_time_research
    context['total_time_misc'] = total_time_misc

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
                    context['children'][index]['children'].append({'name': course_task.name, 'status': 'Ongoing'})
                elif course_task.task_info.status == 1:
                    context['children'][index]['children'].append({'name': course_task.name, 'status': 'Paused'})
                elif course_task.task_info.status == 2:
                    context['children'][index]['children'].append({'name': course_task.name, 'status': 'Complete'})

            index = index + 1
            if index == len(courses):
                break

    return JsonResponse(context)


def get_on_time_late_tasks(request):
    # context = {}
    # courses = Course.objects.filter(user=request.user)
    # research_work = Research.objects.filter(user=request.user)
    # context['research'] = []

    # for course in courses:
    #     context[course.course_name] = []

    # for research in research_work:
    #     if research.task_info.status == 2:
    #         expected_finish_datetime = datetime.datetime.combine(research.task_info.expected_finish_date,
    #                                                              research.task_info.expected_finish_time
    #                                                              .replace(tzinfo=timezone.get_current_timezone()))
    #         if research.task_info.stop_time > expected_finish_datetime:
    #             context['research'].append({'time_exceeded_tasks': {'research_id': research.id,
    #                                                                 'research_topic': research.topic}})
    #         else:
    #             context['research'].append({'on_time_tasks': {'research_id': research.id,
    #                                                           'research_topic': research.topic}})
    # for course in courses:
    #     course_tasks = CourseTask.objects.filter(course=course)
    #     for course_task in course_tasks: 
    #         if course_task.task_info.status == 2:
    #             expected_finish_datetime = datetime.datetime.combine(course_task.task_info.expected_finish_date,
    #                                                                  course_task.task_info.expected_finish_time
    #                                                                  .replace(tzinfo=timezone.get_current_timezone()))
    #             if course_task.task_info.stop_time > expected_finish_datetime:
    #                 context[course.course_name].append({'time_exceeded_tasks': {'task_id': course_task.id,
    #                                                                             'task_name': course_task.name}})
    #             else:
    #                 context[course.course_name].append({'on_time_tasks': {'task_id': course_task.id,
    #                                                                       'task_name': course_task.name}})

    # return JsonResponse(context)
    #context = {[]}
    courses = Course.objects.filter(user=request.user)
    research_work = Research.objects.filter(user=request.user)
    tasks_done_on_time = 0
    tasks_not_done_by_schedule = 0

    for research in research_work:
        if research.task_info.status == 2:
            expected_finish_datetime = datetime.datetime.combine(research.task_info.expected_finish_date,
                                                                research.task_info.expected_finish_time
                                                                .replace(tzinfo=timezone.get_current_timezone()))
            if research.task_info.stop_time > expected_finish_datetime:
                tasks_not_done_by_schedule = tasks_not_done_by_schedule + 1
            else:
                tasks_done_on_time = tasks_done_on_time + 1

    for course in courses:
        course_tasks = CourseTask.objects.filter(course=course)
        for course_task in course_tasks: 
            if course_task.task_info.status == 2:
                expected_finish_datetime = datetime.datetime.combine(course_task.task_info.expected_finish_date,
                                                                      course_task.task_info.expected_finish_time
                                                                      .replace(tzinfo=timezone.get_current_timezone()))
                if course_task.task_info.stop_time > expected_finish_datetime:
                    tasks_not_done_by_schedule = tasks_not_done_by_schedule + 1
                else:
                    tasks_done_on_time = tasks_done_on_time + 1

    #context.append({'label': "Tasks Done On Time", 'value': tasks_done_on_time})
    #context.append({'label': "Tasks Not Done by Schedule", 'value': tasks_not_done_by_schedule})

    return JsonResponse([{'label': "Tasks Done On Time", 'value': tasks_done_on_time}, {'label': "Tasks Not Done by Schedule", 'value': tasks_not_done_by_schedule}], safe=False)


                

