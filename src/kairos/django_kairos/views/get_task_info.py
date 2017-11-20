# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .. models import *
import datetime
from django.http import JsonResponse


# This function returns a dictionary containing {task id: [total time, time spent, percentage completion]}
def get_task_info(request):
    context = {}
    # get all task related information from database
    course_tasks = TaskInfo.objects.filter(coursetask__course__user=request.user).exclude(status=2)
    research_tasks = TaskInfo.objects.filter(research__user=request.user).exclude(status=2)
    misc_tasks = TaskInfo.objects.filter(misc__user=request.user).exclude(status=2)
    tasks = course_tasks | research_tasks | misc_tasks
    for task in tasks:

        start_datetime = datetime.datetime.combine(task.start_date, task.start_time)
        expected_finish_datetime = datetime.datetime.combine(task.expected_finish_date, task.expected_finish_time)
        total_time_in_hours = abs(expected_finish_datetime - start_datetime).total_seconds() / 3600.0

        if task.time_spent is not None:
            if task.continue_time is not None:
                time_spent = ((datetime.datetime.now() - task.continue_time).total_seconds() + task.time_spent) / 3600.0
            else:
                time_spent = ((datetime.datetime.now() - start_datetime).total_seconds() + task.time_spent) / 3600.0
        else:
            time_spent = (datetime.datetime.now() - start_datetime).total_seconds() / 3600.0

        if start_datetime > datetime.datetime.now():
            info = [task.time_needed, abs(time_spent), task.percentage_completion,
                    (time_spent - task.time_needed), total_time_in_hours, '1']
        else:
            info = [task.time_needed, time_spent, task.percentage_completion,
                    (time_spent - task.time_needed), total_time_in_hours, '0']

        context[task.id] = info

    return JsonResponse(context)
