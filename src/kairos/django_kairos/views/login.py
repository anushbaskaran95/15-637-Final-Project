# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from grumblr.forms import UserForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from grumblr.models import UserPosts
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User



def login(request):
	errors = False
	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')

		user = authenticate(email = email, password = password)

		if user:
			login(request, user)
			return HttpResponseRedirect(reverse('dash'))
		else:
			errors = True

		return render(request, 'landing/login.html', {'errors': errors})

@login_required
def logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('logout'))