# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .. import forms


@transaction.atomic
def login(request):
    context = {}
    if request.method == 'GET':
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('dash'))
        else:
            context['form'] = forms.LoginForm()
            return render(request, 'landing/login.html', context)

    form = forms.LoginForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'landing/login.html', context)

    user = authenticate(request, username=form.cleaned_data['username'],
                        password=form.cleaned_data['password'])

    if user is not None:
        auth_login(request, user)
        return HttpResponseRedirect(reverse('dash'))
    else:
        context['errors'] = 'Invalid Credentials'
        return render(request, 'landing/login.html', context)


@login_required
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))
