# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, reverse, get_object_or_404, redirect

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from django.contrib.auth.forms import PasswordChangeForm

from .. models import *
from .. import forms


@login_required
def edit_profile(request, user_id):
    # redirect to user's profile if another user's edit profile is accessed
    if str(user_id) != str(request.user.id):
        return HttpResponseRedirect(reverse('profile'))

    context = dict()
    context['user_id'] = user_id
    context['username'] = request.user.username

    user_instance = get_object_or_404(User, pk=request.user.id)
    if not user_instance:
        raise Http404

    if request.method == 'POST':
        form = forms.EditForm(data=request.POST, instance=user_instance)
        context['form'] = form
        if form.is_valid() and form.check_username(form.cleaned_data, request.user.id):
            form.save()
            messages.success(request, 'Profile changes saved')
            return HttpResponseRedirect(reverse('edit-profile', kwargs={'user_id': request.user.id}))
        else:
            render(request, 'profile/edit-profile.html', context)
    else:
        form = forms.EditForm(instance=user_instance)
        context['form'] = form

    return render(request, 'profile/edit-profile.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was changed')
            return redirect('change-password')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profile/change-password.html', {'form': form, 'username': request.user.username})


