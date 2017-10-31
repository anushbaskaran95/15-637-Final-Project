# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from django.http import HttpResponseRedirect, HttpResponse
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
    return HttpResponse('ok')
