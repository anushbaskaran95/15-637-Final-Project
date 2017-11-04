# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Course(models.Model):
    user = models.ForeignKey(User)
    course_name = models.CharField(max_length=100)


class TaskInfo(models.Model):
    start_date = models.DateField()
    start_time = models.TimeField()
    expected_finish_date = models.DateField()
    expected_finish_time = models.TimeField()
    due_date = models.DateField(null=True, blank=True)
    due_time = models.TimeField(null=True, blank=True)
    comments = models.CharField(max_length=450, null=True, blank=True)
    percentage_completion = models.IntegerField(null=True, blank=True)
    date_paused = models.DateField(null=True, blank=True)
    time_paused = models.TimeField(null=True, blank=True)
    status = models.IntegerField(default=0, null=True, blank=True)


class CourseTask(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_in_task")
    name = models.CharField(max_length=100)
    task_info = models.ForeignKey(TaskInfo)


class Research(models.Model):
    user = models.ForeignKey(User)
    topic = models.CharField(max_length=100)
    task_info = models.ForeignKey(TaskInfo)


class Misc(models.Model):
    user = models.ForeignKey(User)
    task_name = models.CharField(max_length=100)
    task_info = models.ForeignKey(TaskInfo)
