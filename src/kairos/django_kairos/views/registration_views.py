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
@transaction.atomic
def register(request):
    context = {}
    if request.method == 'GET':
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('dash'))
        else:
            context['form'] = forms.RegisterForm()
            return render(request, 'registration/register.html', context)

    form = forms.RegisterForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'registration/register.html', context)

    new_user = form.save(commit=False)
    new_user.is_active = False
    new_user.save()

    token = default_token_generator.make_token(new_user)

    email_body = """Welcome to Kairos. Please click the link below to verify your 
        email address and complete the registration of your account: http://%s%s""" \
                 % (request.get_host(), reverse('confirm-registration',
                                                args=(urlsafe_base64_encode(force_bytes(new_user.pk)), token)))

    send_mail(subject="Verify your Kairos account",
              message=email_body,
              from_email="aburde@andrew.cmu.edu",
              recipient_list=[new_user.email])

    context['email'] = form.cleaned_data['email']
    return render(request, 'registration/needs_confirmation.html', context)


@transaction.atomic
def confirm_registration(request, user_id, token):
    try:
        uid = force_text(urlsafe_base64_decode(user_id))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/email_confirmed.html')
    else:
        return HttpResponse('Activation link is invalid!')


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
    return render(request, 'child/change_password.html', {'form': form})

