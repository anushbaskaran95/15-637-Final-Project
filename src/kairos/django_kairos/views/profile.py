# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.template.loader import render_to_string

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

from django.db import transaction

from django.contrib.auth.models import User

from django.contrib.auth.tokens import default_token_generator

from .. import forms

@login_required
def view_profile(request):
	return render(request, 'profile/profile.html', {})

@login_required
def edit_student_profile(request, username):
	user_instance = get_object_or_404(User, username=username)

	if request.method == 'GET':
		initial_edit_form = StudentEditForm(instance=user_instance)
		return render(request, 'profile/edit-profile.html', {'edit_form': initial_edit_form})

	if request.method == 'POST':
		user_form = StudentEditForm(data=request.POST, instance=user_instance)

		if user_form.is_valid():
			user_form.save()

	return HttpResponseRedirect(reverse('profile'))