# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Course(models.Model):
    user = models.ForeignKey(User)
    # Course Name
    course_name = models.CharField(max_length=100)


class TaskInfo(models.Model):
    # Task start date and time
    start_date = models.DateField()
    start_time = models.TimeField()

    # User defined expected finish date and time
    expected_finish_date = models.DateField()
    expected_finish_time = models.TimeField()

    # Due date and time - optional
    due_date = models.DateField(null=True, blank=True)
    due_time = models.TimeField(null=True, blank=True)

    # Task comments - optional
    comments = models.CharField(max_length=450, null=True, blank=True)

    # Task Percent Complete - optional
    percentage_completion = models.IntegerField(null=True, blank=True)

    # Date and time User pauses the task
    #date_paused = models.DateField(null=True, blank=True)
    #time_paused = models.TimeField(null=True, blank=True)

    # Running record of time spent on task
    #time_spent = models.FloatField(null=True, blank=True)

    # Status of Task (0: Running, 1: Paused, 2: Complete)
    status = models.IntegerField(default=0, null=True, blank=True)


class CourseTask(models.Model):
    # Course under which this task is added
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_tasks")
    # Task Name - should be unique under a course
    name = models.CharField(max_length=100)
    # Info for this task
    task_info = models.ForeignKey(TaskInfo)


class Research(models.Model):
    user = models.ForeignKey(User)
    # Research topic
    topic = models.CharField(max_length=100)
    # Info for this task
    task_info = models.ForeignKey(TaskInfo)


class Misc(models.Model):
    user = models.ForeignKey(User)
    # Routine task name
    task_name = models.CharField(max_length=100)
    # Info for this task
    task_info = models.ForeignKey(TaskInfo)
