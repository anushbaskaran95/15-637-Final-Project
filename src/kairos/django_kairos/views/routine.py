# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse, get_object_or_404

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404, QueryDict
from django.core.mail import send_mail

from django.contrib import messages

# decorator for built-in auth system
from django.contrib.auth.decorators import login_required

from django.db import transaction

from .. forms import *
from .. models import *


# Create your views here.
@login_required
def routine(request):
    context = {}
    routine_form = MiscForm()
    task_info_form = TaskInfoForm()
    context['routine_form'] = routine_form
    context['task_info_form'] = task_info_form
    context['username'] = request.user.username
    context['finished_tasks'] = []
    context['other_tasks'] = []

    tasks = Misc.objects.filter(user=request.user)
    for task in tasks:
        if task.task_info.status == 2:
            context['finished_tasks'].append(task)
        else:
            context['other_tasks'].append(task)

    return render(request, 'dashboard/routine.html', context)


@login_required
@transaction.atomic
def add_routine_task(request):
    if request.method == 'POST':
        routine_form = MiscForm(request.POST)
        task_info_form = TaskInfoForm(request.POST)

        if routine_form.is_valid() and task_info_form.is_valid():
            task_info = task_info_form.save()
            routine_task = routine_form.save(commit=False)
            routine_task.user = request.user
            task_info.expected_finish_notified = False
            task_info.due_notified = False
            routine_task.task_info = task_info
            routine_task.save()
            return JsonResponse({'status': 'ok', 'errors': [], 'task_id': task_info.id})
        else:
            error_list = dict()
            if task_info_form['time_needed'].errors:
                error_list['time_needed-error'] = task_info_form['time_needed'].errors
            if task_info_form['start_date'].errors:
                error_list['start-date-error'] = task_info_form['start_date'].errors
            if task_info_form['expected_finish_date']:
                error_list['finish-date-error'] = task_info_form['expected_finish_date'].errors
            return JsonResponse({'status': 'fail', 'errors': error_list})
    else:
        return HttpResponseRedirect(reverse('dash'))


@login_required
@transaction.atomic
def edit_routine_task(request):
    if request.method == 'POST':
        task = get_object_or_404(Misc, pk=request.POST['task_id'])
        if not task:
            raise Http404

        task_info = get_object_or_404(TaskInfo, pk=request.POST['task_info_id'])
        if not task_info:
            raise Http404

        if 'form' not in request.POST:
            raise Http404

        form = QueryDict(request.POST['form'].encode('ASCII'))
        routine_task_form = MiscForm(form, instance=task)
        task_info_form = TaskInfoForm(form, instance=task_info)

        if routine_task_form.is_valid() and task_info_form.is_valid():
            task = routine_task_form.save()
            task_info = task_info_form.save()
            task.task_info = task_info
            task.save()
            return JsonResponse({'status': 'ok', 'errors': []})
        else:
            error_list = dict()
            if task_info_form['time_needed'].errors:
                error_list['time_needed-error'] = task_info_form['time_needed'].errors
            if task_info_form['start_date'].errors:
                error_list['start-date-error'] = task_info_form['start_date'].errors
            if task_info_form['expected_finish_date'].errors:
                error_list['finish-date-error'] = task_info_form['expected_finish_date'].errors
            return JsonResponse({'status': 'fail', 'errors': error_list})

    else:
        return HttpResponseRedirect(reverse('dash'))
