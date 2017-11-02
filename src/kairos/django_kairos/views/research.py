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
	print "heya"
	context = {}
	if request.method == 'POST':
		print "yolo"
		researchform = forms.ResearchForm(data=request.POST)
		taskinfoform = forms.TaskInfoForm(data=request.POST)
		context['researchform'] = researchform
		context['taskinfoform'] = taskinfoform
		
		if researchform.is_valid() and taskinfoform.is_valid():
			taskinfo = taskinfoform.save()
			research = researchform.save(commit=False)
			research.user = request.user
			research.task_info = taskinfo
			research.save()
			print "heya"
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		else:
			return JsonResponse({'success': False, 'errors': [(k, v[0]) for k, v in researchform.errors.items()] + [(k, v[0]) for k, v in taskinfoform.errors.items()]})
