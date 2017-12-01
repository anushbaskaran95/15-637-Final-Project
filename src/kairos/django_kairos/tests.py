# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client
from django.utils import timezone
from .forms import *


# Create your tests here.
class TestUrls(TestCase):

    def test_login(self):
        client = Client()
        response = client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        client = Client()
        response = client.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_dash(self):
        client = Client()
        user = User.objects.create(username='testuser')
        user.set_password('password')
        user.save()

        client.login(username='testuser', password='password')
        response = client.get('')
        self.assertEqual(response.status_code, 200)

    def test_coursework(self):
        client = Client()
        response = client.get('/course-work')
        self.assertEqual(response.status_code, 302)

    def test_get_task_info(self):
        client = Client()
        user = User.objects.create(username='testuser')
        user.set_password('password')
        user.save()

        client.login(username='testuser', password='password')
        response = client.get('/get-task-info')
        self.assertEqual(response.status_code, 200)

    def test_analytics(self):
        client = Client()
        response = client.get('/analytics')
        self.assertEqual(response.status_code, 302)

    def test_course_analytics(self):
        client = Client()
        user = User.objects.create(username='testuser')
        user.set_password('password')
        user.save()

        client.login(username='testuser', password='password')
        response = client.get('/course-analytics')
        self.assertEqual(response.status_code, 200)


class TestForms(TestCase):

    def test_course_form(self):

        course_name = "Course 1"
        form = CourseForm({'course_name': course_name})
        self.assertTrue(form.is_valid())

        course_name = 'This is a very long text that should not be accepted by the model as a course name. test test test test blah blah'
        form = CourseForm({'course_name': course_name})
        self.assertFalse(form.is_valid())

    def test_course_task_form(self):

        task_name = 'Task 1'
        data = {'name': task_name}
        form = CourseTaskForm(data=data)
        self.assertTrue(form.is_valid())

        task_name = 'This is a very long text that should not be accepted by the model as a task name. test test test test blah blah'
        data = {'name': task_name}
        form = CourseTaskForm(data=data)
        self.assertFalse(form.is_valid())

    def test_task_info_form(self):
        start_date = timezone.now().date()
        start_time = timezone.now().time()

        expected_finish = timezone.now() + timezone.timedelta(days=5)
        expected_finish_date = expected_finish.date()
        expected_finish_time = expected_finish.time()

        time_needed = 12
        due_date = expected_finish_date
        due_time = expected_finish_time

        data = {'start_date': start_date, 'start_time': start_time,
                'expected_finish_date': expected_finish_date, 'expected_finish_time': expected_finish_time,
                'time_needed': time_needed, 'due_date': due_date, 'due_time': due_time, 'comments': ''}

        form = TaskInfoForm(data=data)
        self.assertTrue(form.is_valid())

        expected_finish = timezone.now() - timezone.timedelta(days=5)
        expected_finish_date = expected_finish.date()
        expected_finish_time = expected_finish.time()

        data = {'start_date': start_date, 'start_time': start_time,
                'expected_finish_date': expected_finish_date, 'expected_finish_time': expected_finish_time,
                'time_needed': time_needed, 'due_date': due_date, 'due_time': due_time, 'comments': ''}

        form = TaskInfoForm(data=data)
        self.assertFalse(form.is_valid())


class TestModels(TestCase):

    def test_create_course(self):
        client = Client()
        user = User.objects.create(username='testuser')
        user.set_password('password')
        user.save()

        client.login(username='testuser', password='password')

        course_name = 'Course 2'
        response = client.post('/add-course', {'course_name': course_name})

        self.assertEqual(response.status_code, 200)

        self.assertTrue(len(Course.objects.filter(user=user,
                                                  course_name__iexact='Course 2')) == 1)

        response = client.post('/add-course', {'course_name': course_name})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(Course.objects.filter(user=user,
                                                  course_name__iexact='Course 2')) == 1)

        response = client.post('/add-course', {'course_name': 'Course 1'})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(Course.objects.filter(user=user)) == 2)

    def test_create_course_task(self):
        client = Client()
        user = User.objects.create(username='testuser')
        user.set_password('password')
        user.save()

        client.login(username='testuser', password='password')

        course = Course(user=user, course_name='Test Course')
        course.save()

        self.assertTrue(len(Course.objects.filter(user=user,
                                                  course_name__iexact='Test Course')) == 1)

        start_date = timezone.now().date()
        start_time = timezone.now().time()
        start_time = start_time.strftime('%H:%M')

        expected_finish = timezone.now() + timezone.timedelta(days=5)
        expected_finish_date = expected_finish.date()
        expected_finish_time = expected_finish.time()
        expected_finish_time = expected_finish_time.strftime('%H:%M')

        time_needed = 12.0

        data = {'start_date': start_date, 'start_time': start_time,
                'expected_finish_date': expected_finish_date, 'expected_finish_time': expected_finish_time,
                'time_needed': time_needed, 'comments': '',
                'course_name': course.course_name, 'name': 'Task 1'}

        form = TaskInfoForm(data=data)
        self.assertTrue(form.is_valid())

        form = CourseTaskForm(data=data)
        self.assertTrue(form.is_valid())

        response = client.post('/add-course-task', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(CourseTask.objects.filter(name__exact='Task 1')), 1)

        response = client.post('/add-course-task', data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(len(CourseTask.objects.filter(name__exact='Task 1')) == 2)
        self.assertEqual(len(CourseTask.objects.filter(name__exact='Task 1')), 1)

    def test_create_research_task(self):
        client = Client()
        user = User.objects.create(username='testuser')
        user.set_password('password')
        user.save()

        client.login(username='testuser', password='password')

        start_date = timezone.now().date()
        start_time = timezone.now().time()

        expected_finish = timezone.now() + timezone.timedelta(days=5)
        expected_finish_date = expected_finish.date()
        expected_finish_time = expected_finish.time()

        time_needed = 12
        due_date = expected_finish_date
        due_time = expected_finish_time

        data = {'topic': 'Research 1', 'start_date': start_date, 'start_time': start_time,
                'expected_finish_date': expected_finish_date, 'expected_finish_time': expected_finish_time,
                'time_needed': time_needed, 'due_date': due_date, 'due_time': due_time, 'comments': ''}

        form = TaskInfoForm(data=data)
        self.assertTrue(form.is_valid())

        form = ResearchForm(data=data)
        self.assertTrue(form.is_valid())

        response = client.post('/add-research-task', data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(Research.objects.filter(topic__iexact='Research 1')) == 1)

        data['topic'] = 'reSeaRch 1'

        response = client.post('/add-research-task', data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(Research.objects.filter(topic__iexact='Research 1')) == 1)

