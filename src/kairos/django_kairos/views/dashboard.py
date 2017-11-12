# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse

from django.http import HttpResponseRedirect, HttpResponse

from django.contrib import messages

# decorator for built-in auth system
from django.contrib.auth.decorators import login_required

from django.db import transaction

from django.contrib.auth.models import User

from .. import forms
from .. import models


# Create your views here.
@login_required
def dashboard(request):
    context = {}
    add_course_form = forms.CourseForm()
    course_task_form = forms.CourseTaskForm()
    research_form = forms.ResearchForm()
    routine_form = forms.MiscForm()
    task_info_form = forms.TaskInfoForm()
    context['add_course_form'] = add_course_form
    context['course_task_form'] = course_task_form
    context['research_form'] = research_form
    context['routine_form'] = routine_form
    context['task_info_form'] = task_info_form
    context['courses'] = models.Course.objects.exclude(course_tasks__task_info__status=2)
    context['research_tasks'] = models.Research.objects.exclude(task_info__status=2)
    context['routine_tasks'] = models.Misc.objects.exclude(task_info__status=2)
    context['username'] = request.user.username
    return render(request, 'dashboard/current_tasks.html', context)


def edit_course_modal(request, task_id, task_info_id):
    return HttpResponse('')


def edit_research_modal(request, task_id, task_info_id):
    return HttpResponse('')


def edit_routine_modal(request, task_id, task_info_id):
    return HttpResponse('')
