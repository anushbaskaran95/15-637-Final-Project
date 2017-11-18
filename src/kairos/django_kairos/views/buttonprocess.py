# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404

from .. models import *
import datetime
from django.utils import timezone


def process_button(request):
    #print ("hi")
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        status = request.POST.get('status')
        #print task_id
        print status

        task_info = get_object_or_404(TaskInfo, pk=task_id)
        if not task_info:
            raise Http404

        print type(timezone.now())
        print type(task_info.continue_time)
        print task_info.continue_time
        print task_info.time_spent

        if status == 'false':
            if task_info.continue_time is None:
                task_info.continue_time = datetime.datetime.combine(task_info.start_date, task_info.start_time)
            
            task_info.time_spent = (timezone.now() - task_info.continue_time).total_seconds() + task_info.time_spent

            task_info.status = 1
            task_info.save()

        if status == 'true':
            task_info.continue_time = timezone.now()
            task_info.status = 0
            task_info.save()

    return HttpResponse('')


def process_stop(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')

        task_info = get_object_or_404(TaskInfo, pk=task_id)
        if not task_info:
            raise Http404

        if task_info.continue_time is None:
                task_info.continue_time = datetime.datetime.combine(task_info.start_date, task_info.start_time)
        
        task_info.time_spent = (timezone.now() - task_info.continue_time).total_seconds() + task_info.time_spent
    
        task_info.stop_time = timezone.now()
        task_info.status = 2
        task_info.save()

    return HttpResponse('')
