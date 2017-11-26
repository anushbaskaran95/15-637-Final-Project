# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .. models import *
import datetime

from django.http import JsonResponse


def get_notification_expected_finish(request):
    context = {}
    course_tasks = TaskInfo.objects.filter(coursetask__course__user=request.user).exclude(status=2)
    research_tasks = TaskInfo.objects.filter(research__user=request.user).exclude(status=2)
    misc_tasks = TaskInfo.objects.filter(misc__user=request.user).exclude(status=2)

    for task in course_tasks:
        expected_finish_datetime = datetime.datetime.combine(task.expected_finish_date, task.expected_finish_time)
        time_difference = expected_finish_datetime - datetime.datetime.now()
        time_difference_hour = time_difference.days * 24 + time_difference.seconds / 3600.0

        course_task = CourseTask.objects.get(task_info__id = task.id)

        if (0 < time_difference_hour <= 24) and not task.expected_finish_notified:
            task.expected_finish_notified = True
            task.save()
            context[task.id] = course_task.name + " is approaching the set expected finish time"

    for task in research_tasks:
        expected_finish_datetime = datetime.datetime.combine(task.expected_finish_date, task.expected_finish_time)
        time_difference = expected_finish_datetime - datetime.datetime.now()
        time_difference_hour = time_difference.days * 24 + time_difference.seconds / 3600.0
        research_task =  Research.objects.get(task_info__id= task.id)

        if (0 < time_difference_hour <= 24) and not task.expected_finish_notified:
            task.expected_finish_notified = True
            task.save()
            context[task.id] = research_task.topic + " is approaching set expected finish time"

    for task in misc_tasks:
        expected_finish_datetime = datetime.datetime.combine(task.expected_finish_date, task.expected_finish_time)
        time_difference = expected_finish_datetime - datetime.datetime.now()
        time_difference_hour = time_difference.days * 24 + time_difference.seconds / 3600.0
        misc_task = Misc.objects.get(task_info__id=task.id)

        if (0 < time_difference_hour <= 24) and not task.expected_finish_notified:
            task.expected_finish_notified = True
            task.save()
            context[task.id] = misc_task.task_name + " is approaching set expected finish time"

    return JsonResponse(context)


def get_notification_due(request):
        context = {}
        course_tasks = TaskInfo.objects.filter(coursetask__course__user=request.user).exclude(status=2)
        research_tasks = TaskInfo.objects.filter(research__user=request.user).exclude(status=2)
        misc_tasks = TaskInfo.objects.filter(misc__user=request.user).exclude(status=2)

        for task in course_tasks:
            if task.due_date and task.due_time:
                due_datetime = datetime.datetime.combine(task.due_date, task.due_time)
                time_difference = due_datetime - datetime.datetime.now()
                time_difference_hour = time_difference.days * 24 + time_difference.seconds / 3600.0

                course_task = CourseTask.objects.get(task_info__id = task.id)
                if 0 < time_difference_hour <= 24 and not task.due_notified:
                    task.due_notified = True
                    task.save()
                    context[task.id] = course_task.name + " is approaching the due date"

        for task in research_tasks:
            if task.due_date and task.due_time:
                due_datetime = datetime.datetime.combine(task.due_date, task.due_time)
                time_difference = due_datetime - datetime.datetime.now()
                time_difference_hour = time_difference.days * 24 + time_difference.seconds / 3600.0
                research_task =  Research.objects.get(task_info__id= task.id)
                if 0 < time_difference_hour <= 24 and not task.due_notified:
                    task.due_notified = True
                    task.save()
                    context[task.id] = research_task.topic + " is approaching the due date"

        for task in misc_tasks:
            if task.due_date and task.due_time:
                due_datetime = datetime.datetime.combine(task.due_date, task.due_time)
                time_difference = due_datetime - datetime.datetime.now()
                time_difference_hour = time_difference.days * 24 + time_difference.seconds / 3600.0
                misc_task = Misc.objects.get(task_info__id=task.id)
                if 0 < time_difference_hour <= 24 and not task.due_notified:
                    task.due_notified = True
                    task.save()
                    context[task.id] = misc_task.task_name + " is approaching the due date"

        return JsonResponse(context)
