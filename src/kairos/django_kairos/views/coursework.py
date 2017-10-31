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
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'modals/add_course_modal.html', context)

@login_required
def add_course_task(request):
    context = {}
    if request.method == 'POST':
        courseselected = request.POST.get('course_name')
        course = models.Course.objects.get(course_name=courseselected)
        taskForm = forms.CourseTaskForm(data = request.POST)
        context['taskForm'] = taskForm
        taskInfoForm = forms.TaskInfoForm(data = request.POST)
        context['taskInfoForm'] = taskInfoForm

        task = taskForm.save(commit = False)

        if CourseTask.objects.filter(course=course).filter(name=task.name).exists():
            context['error'] = 'Task for the course already exists'
            return render(request, 'modals/course_modal.html', context) 

        if taskForm.is_valid() and taskInfoForm.is_valid():
            taskinfo = taskInfoForm.save(commit=False)
            taskinfo.save()
            task.task_info = taskinfo
            task.course = courseselected
            task.save()
            print "done"
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'modals/course_modal.html', context)
