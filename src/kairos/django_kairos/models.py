# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Course(models.Model):
	user = models.ForeignKey(User)
	course_name = models.CharField(max_length = 100)

class TaskInfo(models.Model):
	start_time = models.DateTimeField()
	expected_finish_time = models.DateTimeField()
	due_date = models.DateTimeField(null = True)
	comments = models.CharField(max_length = 450, null = True)
	percentage_completion = models.IntegerField()


class CourseTask(models.Model):
	course = models.ForeignKey(Course)
	name = models.CharField(max_length = 100)
	task_info = models.ForeignKey(TaskInfo)
	

class Research(models.Model):
	user = models.ForeignKey(User)
	topic = models.CharField(max_length = 100)
	task_info = models.ForeignKey(TaskInfo)

class Misc(models.Model):
	user = models.ForeignKey(User)
	task_name = models.CharField(max_length = 100)
	task_info = models.ForeignKey(TaskInfo)

class Custom(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length = 50)

class CustomTask(models.Model):
	custom_field = models.ForeignKey(Custom)
	name = models.CharField(max_length = 100)
	task_info = models.ForeignKey(TaskInfo)


