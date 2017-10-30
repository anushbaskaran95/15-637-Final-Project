# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, reverse, get_object_or_404

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash


from django.contrib.auth.models import User

from django.contrib.auth.forms import PasswordChangeForm


from .. import forms


@login_required
def view_profile(request):
	return render(request, 'profile/profile.html', {})


@login_required
def edit_student_profile(request, username):
	user_instance = get_object_or_404(User, username=username)

	if request.method == 'GET':
		initial_edit_form = forms.StudentEditForm(instance=user_instance)
		return render(request, 'profile/edit-profile.html', {'edit_form': initial_edit_form})

	if request.method == 'POST':
		user_form = forms.StudentEditForm(data=request.POST, instance=user_instance)

		if user_form.is_valid():
			user_form.save()

	return HttpResponseRedirect(reverse('profile'))


@login_required
def change_password(request):
	if request.method == 'POST':
		password_changed_form = PasswordChangeForm(data=request.POST, user=request.user)

		if password_changed_form.is_valid():
			password_changed_form.save()
			update_session_auth_hash(request, password_changed_form.user)
			return HttpResponseRedirect('dash')

		else:
			return render(request, 'profile/change-password.html', {'cpform': password_changed_form})

	else:
		password_changed_form = PasswordChangeForm(user=request.user)
		return render(request, 'profile/change-password.html', {'cpform': password_changed_form})