# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse, get_object_or_404

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404, QueryDict

from django.contrib import messages

# decorator for built-in auth system
from django.contrib.auth.decorators import login_required

from django.db import transaction

from .. forms import *
from .. models import *


# Create your views here.
@login_required
def research(request):
    context = {}
    research_form = ResearchForm()
    task_info_form = TaskInfoForm()
    context['research_form'] = research_form
    context['task_info_form'] = task_info_form
    context['research_tasks'] = list(Research.objects.filter(user=request.user).order_by('-task_info__expected_finish_date'))
    context['username'] = request.user.username
    return render(request, 'dashboard/research.html', context)


@login_required
def add_research_task(request):
    if request.method == 'POST':
        research_form = ResearchForm(request.POST)
        task_info_form = TaskInfoForm(request.POST)

        if research_form.is_valid() and task_info_form.is_valid():
            task_info = task_info_form.save()
            research_task = research_form.save(commit=False)
            research_task.user = request.user
            research_task.task_info = task_info
            research_task.save()
            return JsonResponse({'status': 'ok', 'errors': []})
        else:
            error_list = dict()
            if research_form['topic'].errors:
                error_list['topic-error'] = research_form['topic'].errors
            if task_info_form['time_needed'].errors:
                error_list['time_needed-error'] = task_info_form['time_needed'].errors
            if task_info_form['start_date'].errors:
                error_list['start-date-error'] = task_info_form['start_date'].errors
            if task_info_form['expected_finish_date']:
                error_list['finish-date-error'] = task_info_form['expected_finish_date'].errors
            if task_info_form['due_date']:
                error_list['due-date-error'] = task_info_form['due_date'].errors
            return JsonResponse({'status': 'fail', 'errors': error_list})
    else:
        return HttpResponseRedirect(reverse('dash'))


@login_required
def edit_research_task(request):
    if request.method == 'POST':
        task = get_object_or_404(Research, pk=request.POST['task_id'])
        if not task:
            raise Http404

        task_info = get_object_or_404(TaskInfo, pk=request.POST['task_info_id'])
        if not task_info:
            raise Http404

        form = QueryDict(request.POST['form'].encode('ASCII'))
        research_task_form = ResearchForm(form, instance=task)
        task_info_form = TaskInfoForm(form, instance=task_info)

        if research_task_form.is_valid() and task_info_form.is_valid():
            task = research_task_form.save()
            task_info = task_info_form.save()
            task.task_info = task_info
            task.save()
            return JsonResponse({'status': 'ok', 'errors': []})
        else:
            error_list = dict()
            if research_task_form['topic'].errors:
                error_list['topic-error'] = research_task_form['topic'].errors
            if task_info_form['time_needed'].errors:
                error_list['time_needed-error'] = task_info_form['time_needed'].errors
            if task_info_form['start_date'].errors:
                error_list['start-date-error'] = task_info_form['start_date'].errors
            if task_info_form['expected_finish_date'].errors:
                error_list['finish-date-error'] = task_info_form['expected_finish_date'].errors
            if task_info_form['due_date'].errors:
                error_list['due-date-error'] = task_info_form['due_date'].errors
            if task_info_form['percentage_completion'].errors:
                error_list['pc-error'] = task_info_form['percentage_completion'].errors
            return JsonResponse({'status': 'fail', 'errors': error_list})

    else:
        return HttpResponseRedirect(reverse('dash'))
