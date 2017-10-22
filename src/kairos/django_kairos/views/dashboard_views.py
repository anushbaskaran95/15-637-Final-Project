<<<<<<< HEAD:src/kairos/django_kairos/views.py
||||||| merged common ancestors
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.utils import timezone

from django.core.mail import send_mail

# decorator for built-in auth system
from django.contrib.auth.decorators import login_required

from django.db import transaction
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

# used to create and manually log in a user
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, logout

from django.contrib.auth.tokens import default_token_generator

from forms import *


# Create your views here.
@login_required
def dashboard(request):
    return


def login(request):
    return


def logout_user(request):
    return


@transaction.atomic
def register(request):
    return


@transaction.atomic
def confirm_registration(request, user_id, token):
    return


@login_required
def edit_profile(request, user_id):
    return


@login_required
def change_password(request):
    return
=======
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
def home(request):
    return HttpResponseRedirect(reverse('dash'))


def dashboard(request):
    return HttpResponseRedirect('Dashboard')
>>>>>>> origin/advait:src/kairos/django_kairos/views/dashboard_views.py
