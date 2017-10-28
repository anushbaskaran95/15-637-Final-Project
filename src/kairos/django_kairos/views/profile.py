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