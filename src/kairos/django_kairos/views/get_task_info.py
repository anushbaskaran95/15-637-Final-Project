# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse, Http404

from django.contrib import messages

# decorator for built-in auth system
from django.contrib.auth.decorators import login_required

from django.db import transaction

from django.contrib.auth.models import User

from .. forms import *
from .. models import *
import datetime
from django.utils import timezone

#import json
from django.http import JsonResponse

# This function returns a dictionary containing {task id: [total time, time spent, percentage completion]}
def get_task_info(arg):
    context = {}
    tasks = TaskInfo.objects.exclude(status = 2)
    for task in tasks:
        start_datetime = datetime.datetime.combine(task.start_date, task.start_time)
        expected_finish_datetime = datetime.datetime.combine(task.expected_finish_date, task.expected_finish_time)
        total_time_in_hours = abs(expected_finish_datetime - start_datetime).total_seconds() / 3600.0
        if task.time_spent is not None:
            time_spent = (datetime.datetime.now() - task.continue_time) + task.time_spent
        else:
            time_spent = (datetime.datetime.now() - task.continue_time)
        time_spent = abs(time_spent).total_seconds() /3600.0

        info = [total_time_in_hours, time_spent, task.percentage_completion]
        context[task.id] = info

    return JsonResponse(context)
