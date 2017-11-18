# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .. models import *
import datetime
from django.http import JsonResponse


# This function returns a dictionary containing {task id: [total time, time spent, percentage completion]}
def get_task_info(request):
    context = {}
    tasks = TaskInfo.objects.exclude(status=2)
    for task in tasks:
        start_datetime = datetime.datetime.combine(task.start_date, task.start_time)
        expected_finish_datetime = datetime.datetime.combine(task.expected_finish_date, task.expected_finish_time)
        total_time_in_hours = abs(expected_finish_datetime - start_datetime).total_seconds() / 3600.0
        if task.time_spent is not None:
            time_spent = (datetime.datetime.now() - task.continue_time) + task.time_spent
        else:
            time_spent = (datetime.datetime.now() - start_datetime)
        time_spent = abs(time_spent).total_seconds() / 3600.0

        info = [total_time_in_hours, time_spent, task.percentage_completion]
        context[task.id] = info

    return JsonResponse(context)
