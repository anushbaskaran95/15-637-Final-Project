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
from .. import utils


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
    context['username'] = request.user.username
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
            return JsonResponse({'status': 'fail', 'errors': [{k: v[0]} for k, v in course_form.errors.items()]})


@login_required
def add_course_task(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        course = models.Course.objects.filter(course_name__exact=course_name)[0]

        if not course:
            return JsonResponse({'status': 'fail', 'errors': [{'course-name-error': 'Course does not exist'}]})

        if 'name' in request.POST:
            if course.course_in_task.filter(name__iexact=request.POST['name']):
                return JsonResponse({'status': 'fail', 'errors': {'task-name-error': 'Task already exists'}})
        else:
            return JsonResponse({'status': 'fail', 'errors': {'task-name-error': 'Enter task name'}})

        course_task_form = forms.CourseTaskForm(request.POST)
        task_info_form = forms.TaskInfoForm(request.POST)
        task = course_task_form.save(commit=False)

        if course_task_form.is_valid() and task_info_form.is_valid():
            task_info = task_info_form.save()
            task.task_info = task_info
            task.course = course
            task.save()
            return JsonResponse({'status': 'ok', 'errors': []})
        else:
            error_list = dict()
            error_list['status'] = 'fail'
            if task_info_form['start_date'].errors:
                error_list['start-date-error'] = task_info_form['start_date'].errors[0]
            if task_info_form['expected_finish_date']:
                error_list['finish-date-error'] = task_info_form['expected_finish_date'].errors[0]
            if task_info_form['due_date']:
                error_list['due-date-error'] = task_info_form['due_date'].errors[0]
            return JsonResponse({'status': 'fail', 'errors': error_list})
    else:
        return HttpResponseRedirect(reverse('dash'))
