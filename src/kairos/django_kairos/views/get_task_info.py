# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .. models import *
import datetime
from django.http import JsonResponse
from django.utils import timezone


# This function returns a dictionary containing {task id: [total time, time spent, percentage completion]}
def get_task_info(request):
    context = {}
    now = timezone.now()

    # get all task related information from database
    course_tasks = TaskInfo.objects.filter(coursetask__course__user=request.user).exclude(status=2)
    research_tasks = TaskInfo.objects.filter(research__user=request.user).exclude(status=2)
    misc_tasks = TaskInfo.objects.filter(misc__user=request.user).exclude(status=2)
    tasks = course_tasks | research_tasks | misc_tasks

    for task in tasks:

        start_datetime = datetime.datetime.combine(task.start_date,
                                                   task.start_time.replace(tzinfo=timezone.get_current_timezone()))

        expected_finish_datetime = datetime.datetime.combine(task.expected_finish_date,
                                                             task.expected_finish_time
                                                             .replace(tzinfo=timezone.get_current_timezone()))

        total_time_in_hours = (expected_finish_datetime - start_datetime).total_seconds() / 3600.0

        # calculate time spent on ongoing task
        if task.time_spent is not None:
            time_spent = ((now - task.continue_time).total_seconds() + task.time_spent) / 3600.0
        else:
            time_spent = (now - task.continue_time).total_seconds() / 3600.0

        # time spent on paused task is set in DB
        if task.status == 1:
            time_spent = task.time_spent / 3600.0

        if start_datetime > now:
            info = [task.start_date.strftime("%B %d, %Y"), task.start_time.strftime('%H:%M'), 0, 0, 0, '1']
        else:
            info = [task.time_needed, time_spent, task.percentage_completion,
                    (time_spent - task.time_needed), total_time_in_hours, '0']

        if now > expected_finish_datetime:
            info = [task.time_needed, time_spent, task.percentage_completion,
                    (time_spent - task.time_needed), total_time_in_hours, '2']

        context[task.id] = info

    return JsonResponse(context)
