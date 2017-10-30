# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse

from django.http import HttpResponseRedirect, HttpResponse

from django.contrib import messages

# decorator for built-in auth system
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from .. import forms


# Create your views here.
@login_required
def coursework(request):
    context = {}
    add_course_form = forms.CourseForm()
    context['add_course_form'] = add_course_form
    return render(request, 'dashboard/coursework.html', context)


@login_required
def add_course(request):
    return HttpResponse('ok')
