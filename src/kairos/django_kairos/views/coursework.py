# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse

from django.http import HttpResponseRedirect, HttpResponse

from django.contrib import messages

# decorator for built-in auth system
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from .. import forms
from .. import models


# Create your views here.
@login_required
def coursework(request):
    context = {}
    add_course_form = forms.CourseForm()
    course_task_form = forms.CourseTaskForm()
    task_info_form = forms.TaskInfoForm()
    context['add_course_form'] = add_course_form
    context['course_task_form'] = course_task_form
    context['task_info_form'] = task_info_form
    context['courses'] = models.Course.objects.all()
    return render(request, 'dashboard/coursework.html', context)


@login_required
def add_course(request):
    context = {}
    if request.method == 'POST':
        courseform = forms.CourseForm(data = request.POST)
        context['form'] = courseform

        if courseform.is_valid():
            course = courseform.save(commit = False)
            course.user = request.user
            course.save()
            return HttpResponse('')
    
    return render(request, 'modals/add_course_modal.html', context)

@login_required
def add_course_task(request):
    context = {}

    return HttpResponse('ok')
