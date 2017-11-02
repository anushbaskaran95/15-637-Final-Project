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
def routine(request):
    context = {}
    routine_form = forms.MiscForm()
    task_info_form = forms.TaskInfoForm()
    context['routine_form'] = routine_form
    context['task_info_form'] = task_info_form
    return render(request, 'dashboard/routine.html', context)


@login_required
def add_routine_task(request):
	print "heya"
	context = {}
	if request.method == 'POST':
		print "yolo"
		routineform = forms.MiscForm(data=request.POST)
		taskinfoform = forms.TaskInfoForm(data=request.POST)
		context['routineform'] = routineform
		context['taskinfoform'] = taskinfoform
		
		if routineform.is_valid() and taskinfoform.is_valid():
			taskinfo = taskinfoform.save()
			routine = routineform.save(commit=False)
			routine.user = request.user
			routine.task_info = taskinfo
			routine.save()
			print "heya"
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		else:
			return JsonResponse({'success': False, 'errors': [(k, v[0]) for k, v in routineform.errors.items()] + [(k, v[0]) for k, v in taskinfoform.errors.items()]})
