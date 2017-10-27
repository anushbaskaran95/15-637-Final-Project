# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


def login(request):
    errors = False
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('dash'))
        else:
            errors = True

    return render(request, 'landing/login.html', {'errors': errors})


@login_required
def logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
