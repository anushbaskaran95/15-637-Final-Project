# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client
from .models import *


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
        response = client.get('')
        self.assertEqual(response.status_code, 302)

    def test_coursework(self):
        client = Client()
        response = client.get('/course-work')
        self.assertEqual(response.status_code, 302)

    def test_get_task_info(self):
        client = Client()
        response = client.get('/get-task-info')
        self.assertEqual(response.status_code, 302)


class TestModels(TestCase):

    fixtures = ['db']

    # def create_course(self):
    #     return
