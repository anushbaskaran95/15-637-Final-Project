# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.mail import send_mail

from django.contrib import messages

# decorator for built-in auth system
from django.contrib.auth.decorators import login_required

from django.db import transaction

from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth.tokens import default_token_generator

from .. import forms


# Create your views here.
@login_required
def research(request):
    context = {}
    research_form = forms.ResearchForm()
    task_info_form = forms.TaskInfoForm()
    context['research_form'] = research_form
    context['task_info_form'] = task_info_form
    return render(request, 'dashboard/research.html', context)


@login_required
def add_research_task(request):
    if request.method == 'POST':
        research_form = forms.ResearchForm(request.POST)
        task_info_form = forms.TaskInfoForm(request.POST)
		
        if research_form.is_valid() and task_info_form.is_valid():
            task_info = task_info_form.save()
            research_task = research_form.save(commit=False)
            research_task.user = request.user
            research_task.task_info = task_info
            research_task.save()
            return JsonResponse({'status': 'ok', 'errors': []})
        else:
            error_list = dict()
            error_list['status'] = 'fail'
            error_list['topic'] = research_form['topic'].errors[0]
            error_list['start-date-error'] = task_info_form['start_date'].errors[0]
            error_list['finish-date-error'] = task_info_form['expected_finish_date'].errors[0]
            error_list['due-date-error'] = task_info_form['due_date'].errors[0]
            return JsonResponse({'status': 'fail', 'errors': error_list})
    else:
        return HttpResponseRedirect(reverse('dash'))
