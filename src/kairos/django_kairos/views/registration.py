# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, reverse
from django.template.loader import render_to_string

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail

from django.db import transaction

from django.contrib.auth.models import User

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

    email_data = {'domain': request.get_host(), 'token': token,
                  'id': urlsafe_base64_encode(force_bytes(new_user.pk)),
                  'username': new_user.username}

    html_message = render_to_string('registration/confirmation_link.html', email_data)

    send_mail(subject="Verify your Kairos account",
              message='html_message',
              html_message=html_message,
              from_email="kairos.backend@gmail.com",
              recipient_list=[new_user.email])

    context['email'] = register_form.cleaned_data['email']
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

