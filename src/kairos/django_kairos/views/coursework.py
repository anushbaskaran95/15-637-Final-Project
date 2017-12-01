# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404, QueryDict

from django.db import transaction

# decorator for built-in auth system
from django.contrib.auth.decorators import login_required

from .. forms import *
from .. models import *


# Create your views here.
@login_required
def coursework(request):
    context = {}
    add_course_form = CourseForm()
    course_task_form = CourseTaskForm()
    task_info_form = TaskInfoForm()
    context['add_course_form'] = add_course_form
    context['course_task_form'] = course_task_form
    context['task_info_form'] = task_info_form
    context['finished_tasks'] = []
    context['other_tasks'] = []

    courses = Course.objects.filter(user=request.user)
    context['course_names'] = courses

    for course in courses:
        tasks = CourseTask.objects.filter(course=course)
        for task in tasks:
            if task.task_info.status == 2:
                context['finished_tasks'].append(task)
            else:
                context['other_tasks'].append(task)

    context['username'] = request.user.username

    return render(request, 'dashboard/coursework.html', context)


@login_required
@transaction.atomic
def add_course(request):
    context = {}
    if request.method == 'POST':
        course_form = CourseForm(request.POST, user=request.user)
        context['form'] = course_form

        if course_form.is_valid():
            course = course_form.save(commit=False)
            course.user = request.user
            course.save()
            return JsonResponse({'status': 'ok', 'errors': []})
        else:
            return JsonResponse({'status': 'fail', 'errors': [{k: v[0]} for k, v in course_form.errors.items()]})


@login_required
@transaction.atomic
def add_course_task(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        course = Course.objects.filter(user=request.user, course_name__exact=course_name)[0]

        if not course:
            return JsonResponse({'status': 'fail', 'errors': [{'course-name-error': 'Course does not exist'}]})

        if 'name' in request.POST:
            if course.course_tasks.filter(name__iexact=request.POST['name']):
                return JsonResponse({'status': 'fail', 'errors': {'task-name-error': 'Task already exists'}})
        else:
            return JsonResponse({'status': 'fail', 'errors': {'task-name-error': 'Enter task name'}})

        course_task_form = CourseTaskForm(request.POST)
        task_info_form = TaskInfoForm(request.POST)

        if course_task_form.is_valid() and task_info_form.is_valid():
            task = course_task_form.save(commit=False)
            task_info = task_info_form.save()
            task.task_info = task_info
            task.course = course
            task.save()
            return JsonResponse({'status': 'ok', 'errors': [], 'task_id': task_info.id})
        else:
            error_list = dict()
            if task_info_form['time_needed'].errors:
                error_list['time-needed-error'] = task_info_form['time_needed'].errors
            if task_info_form['start_date'].errors:
                error_list['start-date-error'] = task_info_form['start_date'].errors
            if task_info_form['expected_finish_date'].errors:
                error_list['finish-date-error'] = task_info_form['expected_finish_date'].errors
            if task_info_form['due_date'].errors:
                error_list['due-date-error'] = task_info_form['due_date'].errors
            return JsonResponse({'status': 'fail', 'errors': error_list})
    else:
        return HttpResponseRedirect(reverse('dash'))


@login_required
@transaction.atomic
def edit_course_task(request):
    if request.method == 'POST':
        task = get_object_or_404(CourseTask, pk=request.POST['task_id'])
        if not task:
            raise Http404

        task_info = get_object_or_404(TaskInfo, pk=request.POST['task_info_id'])
        if not task_info:
            raise Http404

        if 'form' not in request.POST:
            raise Http404

        form = QueryDict(request.POST['form'].encode('ASCII'))
        course_task_form = CourseTaskForm(form, instance=task)
        task_info_form = TaskInfoForm(form, instance=task_info)

        if form.get('name') != task.name:
            if task.course.course_tasks.filter(name__iexact=form.get('name')):
                return JsonResponse({'status': 'fail', 'errors': {'task-name-error': 'Task already exists'}})

        if course_task_form.is_valid() and task_info_form.is_valid():
            task = course_task_form.save()
            task_info = task_info_form.save()
            task_info.expected_finish_notified = False
            task_info.due_notified = False
            task.task_info = task_info
            task.save()
            return JsonResponse({'status': 'ok', 'errors': []})
        else:
            error_list = dict()
            if task_info_form['time_needed'].errors:
                error_list['time-needed-error'] = task_info_form['time_needed'].errors
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
