# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .. models import *
import datetime

from django.http import JsonResponse
#from django.contrib import messages


def get_notification(request):
    print("hi")
    context = {}
    course_tasks = TaskInfo.objects.filter(coursetask__course__user=request.user).exclude(status=2)
    research_tasks = TaskInfo.objects.filter(research__user=request.user).exclude(status=2)
    misc_tasks = TaskInfo.objects.filter(misc__user=request.user).exclude(status=2)

    for task in course_tasks:
        expected_finish_datetime = datetime.datetime.combine(task.expected_finish_date, task.expected_finish_time)
        time_difference = expected_finish_datetime - datetime.datetime.now()
        time_difference_hour = time_difference.days * 24 + time_difference.seconds / 3600.0
        course_task = CourseTask.objects.get(task_info__id = task.id)
        if time_difference_hour > 0 and time_difference_hour <= 24:
            context[task.id] = course_task.name

    for task in research_tasks:
        expected_finish_datetime = datetime.datetime.combine(task.expected_finish_date, task.expected_finish_time)
        time_difference = expected_finish_datetime - datetime.datetime.now()
        time_difference_hour = time_difference.days * 24 + time_difference.seconds / 3600.0
        research_task =  Research.objects.get(task_info__id= task.id)
        if time_difference_hour > 0 and time_difference_hour <= 24:
            context[task.id] = research_task.topic

    for task in misc_tasks:
        expected_finish_datetime = datetime.datetime.combine(task.expected_finish_date, task.expected_finish_time)
        time_difference = expected_finish_datetime - datetime.datetime.now()
        time_difference_hour = time_difference.days * 24 + time_difference.seconds / 3600.0
        misc_task = Misc.objects.get(task_info__id=task.id)
        if time_difference_hour > 0 and time_difference_hour <= 24:
            context[task.id] = misc_task.task_name


    return JsonResponse(context)
