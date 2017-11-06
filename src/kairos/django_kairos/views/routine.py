# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.mail import send_mail

from django.contrib import messages

# decorator for built-in auth system
from django.contrib.auth.decorators import login_required

from django.db import transaction

from .. import forms
from .. import models


# Create your views here.
@login_required
def routine(request):
    context = {}
    routine_form = forms.MiscForm()
    task_info_form = forms.TaskInfoForm()
    context['routine_form'] = routine_form
    context['task_info_form'] = task_info_form
    context['routine_tasks'] = models.Misc.objects.all()
    context['username'] = request.user.username
    return render(request, 'dashboard/routine.html', context)


@login_required
def add_routine_task(request):
    if request.method == 'POST':
        routine_form = forms.MiscForm(request.POST)
        task_info_form = forms.TaskInfoForm(request.POST)

        if routine_form.is_valid() and task_info_form.is_valid():
            task_info = task_info_form.save()
            routine_task = routine_form.save(commit=False)
            routine_task.user = request.user
            routine_task.task_info = task_info
            routine_task.save()
            return JsonResponse({'status': 'ok', 'errors': []})
        else:
            error_list = dict()
            if task_info_form['start_date'].errors:
                error_list['start-date-error'] = task_info_form['start_date'].errors
            if task_info_form['expected_finish_date']:
                error_list['finish-date-error'] = task_info_form['expected_finish_date'].errors
            return JsonResponse({'status': 'fail', 'errors': error_list})
    else:
        return HttpResponseRedirect(reverse('dash'))
