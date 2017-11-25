# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404

from .. models import *
import datetime
from django.utils import timezone


def process_button(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        status = request.POST.get('status')

        task_info = get_object_or_404(TaskInfo, pk=task_id)
        if not task_info:
            raise Http404

        if status == 'false':
            if task_info.continue_time is None:
                task_info.continue_time = datetime.datetime.combine(task_info.start_date,
                                                                    task_info.start_time.replace(
                                                                        tzinfo=timezone.get_current_timezone()))

            if task_info.time_spent is None:
                task_info.time_spent = (timezone.now() - task_info.continue_time).total_seconds()
            else:
                task_info.time_spent = (timezone.now() - task_info.continue_time).total_seconds() + task_info.time_spent

            task_info.status = 1
            task_info.save()

        if status == 'true':
            task_info.continue_time = timezone.now()
            task_info.status = 0
            task_info.save()

            alltasks = TaskInfo.objects.exclude(pk=task_id).filter(status=0)

            if alltasks is not None:
                for task in alltasks:
                    if task.continue_time is None:
                        task.continue_time = datetime.datetime.combine(task.start_date,
                                                                       task.start_time.replace(tzinfo=timezone.get_current_timezone()))

                    if task.time_spent is None:
                        task.time_spent = (timezone.now() - task.continue_time).total_seconds()
                    else:
                        task.time_spent = (timezone.now() - task.continue_time).total_seconds() + task.time_spent

                    task.status = 1
                    task.save()

    return HttpResponse('')


def process_stop(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')

        task_info = get_object_or_404(TaskInfo, pk=task_id)
        if not task_info:
            raise Http404

        if task_info.continue_time is None:
            task_info.continue_time = datetime.datetime.combine(task_info.start_date, task_info.start_time)

        if task_info.time_spent is None:
            task_info.time_spent = (timezone.now() - task_info.continue_time).total_seconds()
        else:
            task_info.time_spent += (timezone.now() - task_info.continue_time).total_seconds()
    
        task_info.stop_time = timezone.now()
        task_info.status = 2
        task_info.save()

    return HttpResponse('')
