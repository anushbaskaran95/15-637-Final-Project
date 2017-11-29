# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required

from .. models import *
from django.utils import timezone

@login_required
def process_button(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        status = request.POST.get('status')

        task_info = get_object_or_404(TaskInfo, pk=task_id)
        if not task_info:
            raise Http404

        if status == 'false':

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

            all_tasks = TaskInfo.objects.exclude(pk=task_id).filter(status=0)

            if all_tasks is not None:
                for task in all_tasks:
                    if task.time_spent is None:
                        task.time_spent = (timezone.now() - task.continue_time).total_seconds()
                    else:
                        task.time_spent = (timezone.now() - task.continue_time).total_seconds() + task.time_spent

                    task.status = 1
                    task.save()

    return HttpResponse('')

@login_required
def process_stop(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')

        task_info = get_object_or_404(TaskInfo, pk=task_id)
        if not task_info:
            raise Http404

        # time spent on paused task is set in DB
        if task_info.status == 1:
            time_spent = task_info.time_spent
        else:
            if task_info.time_spent is not None:
                time_spent = (timezone.now() - task_info.continue_time).total_seconds() + task_info.time_spent
            else:
                time_spent = (timezone.now() - task_info.continue_time).total_seconds()

        task_info.time_spent = time_spent
        task_info.stop_time = timezone.now()
        task_info.percentage_completion = 100
        task_info.status = 2
        task_info.save()

    return HttpResponse('')
