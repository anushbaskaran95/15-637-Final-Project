# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

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
        course_form = forms.CourseForm(request.POST)
        context['form'] = course_form

        if course_form.is_valid():
            course = course_form.save(commit=False)
            course.user = request.user
            course.save()
            return JsonResponse({'status': 'ok', 'errors': []})
        else:
            return JsonResponse({'status': 'fail', 'errors': [(k, v[0]) for k, v in course_form.errors.items()]})


@login_required
def add_course_task(request):
    #print "hi"
    context = {}
    if request.method == 'POST':
        #print "helllo"
        courseselected = request.POST.get('course_name')
        #print courseselected
        course = courseselected
        taskForm = forms.CourseTaskForm(data = request.POST)
        context['taskForm'] = taskForm
        taskInfoForm = forms.TaskInfoForm(data = request.POST)
        context['taskInfoForm'] = taskInfoForm

        task = taskForm.save(commit = False)
        print task.name

        #taskcourse = models.CourseTask.objects.filter(course_task_course=course)
        #if  taskcourse.filter(name=task.name).exists():
        if models.Course.objects.filter(coursetask__name__exact=task.name):
            context['error'] = 'Task for the course already exists'
            return render(request, 'modals/course_modal.html', context) 

        if taskForm.is_valid() and taskInfoForm.is_valid():
            taskinfo = taskInfoForm.save(commit=False)
            taskinfo.save()
            task.task_info = taskinfo
            task.course = course
            task.save()
            print "done"
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else:
            return JsonResponse({'success': False, 'errors': [(k, v[0]) for k, v in taskForm.errors.items()] + [(k, v[0]) for k, v in taskInfoForm.errors.items()]})