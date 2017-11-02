# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.mail import send_mail

from django.contrib import messages

# decorator for built-in auth system
from django.contrib.auth.decorators import login_required

from django.db import transaction

from django.contrib.auth.tokens import default_token_generator

from .. import forms


# Create your views here.
@login_required
def routine(request):
    context = {}
    routine_form = forms.MiscForm()
    task_info_form = forms.TaskInfoForm()
    context['routine_form'] = routine_form
    context['task_info_form'] = task_info_form
    return render(request, 'dashboard/routine.html', context)


@login_required
def add_routine_task(request):
    context = {}
    if request.method == 'POST':
        routineform = forms.MiscForm(data=request.POST)
        taskinfoform = forms.TaskInfoForm(data=request.POST)
        context['routineform'] = routineform
        context['taskinfoform'] = taskinfoform

        if routineform.is_valid() and taskinfoform.is_valid():
            taskinfo = taskinfoform.save()
            routine_task = routineform.save(commit=False)
            routine_task.user = request.user
            routine_task.task_info = taskinfo
            routine_task.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return JsonResponse({'success': False, 'errors': [(k, v[0]) for k, v in routineform.errors.items()] + [(k, v[0]) for k, v in taskinfoform.errors.items()]})
