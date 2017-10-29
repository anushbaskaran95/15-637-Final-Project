from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

import datetime


# Register Form
class RegisterForm(UserCreationForm):

    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'id': 'email'}))

    first_name = forms.CharField(label='First Name',
                                 widget=forms.TextInput(attrs={'id': 'first_name'}),
                                 max_length=50,
                                 required=False)

    last_name = forms.CharField(label='Last Name',
                                widget=forms.TextInput(attrs={'id': 'last_name'}),
                                max_length=50,
                                required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("This username is already registered")
        else:
            return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError("This email id is already registered")
        else:
            return email

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')

        if commit:
            user.save()
        return user

    def register_user(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        password = self.cleaned_data.get('password')

        new_user = User.objects.create_user(username=username,
                                            email=email,
                                            first_name=first_name,
                                            last_name=last_name,
                                            password=password)
        new_user.save()

        return new_user

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('course_name',)

    def clean_course_name(self):
        course_name = self.cleaned_data.get('course_name')
        if Course.objects.filter(course_name__exact=course_name):
            raise forms.ValidationError("Course name is already existed")
        else:
            return course_name

class TaskInfoForm(forms.ModelForm):
    class Meta:
        model = TaskInfo
        exclude = ('time_spent',)
    """
    def clean_start_time(self):
        start_time = self.cleaned_data.get('start_time')
        now = datetime.datetime.now()
        if start_time < now:
            raise forms.ValidationError("You should plan for future task")
        else:
            return start_time
    """
    def clean_expected_finish_time(self):
        expected_finish_time = self.cleaned_data.get('expected_finish_time')
        start_time = self.cleaned_data.get('start_time')
        if expected_finish_time <= start_time:
            raise forms.ValidationError("Expected finish time should in the future")
        else:
            return expected_finish_time
    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        start_time = self.cleaned_data.get('start_time')
        if expected_finish_time <= start_time:
            raise forms.ValidationError("Due date should in the future")
        else:
            return due_date

    def clean_percentage_completion(self):
        percentage_completion = self.cleaned_data.get('percentage_completion')
        if percentage_completion < 0 or percentage_completion >100:
            forms.ValidationError("invalid percentage completion")
        else:
            return percentage_completion


class CourseTaskForm(forms.ModelForm):
    class Meta:
        model = CourseTask
        fields = ('name',)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if CourseTask.objects.filter(name__exact = name):
            raise forms.ValidationError("This course task is already existed")
        else:
            return name

class ResearchForm(forms.ModelForm):
    class Meta:
        model =  Research
        fields = ('topic',)

    def clean_topic(self):
        topic = self.cleaned_data.get('topic')
        if Research.objects.filter(topic__exact = topic):
            raise forms.ValidationError("This reserch name is already existed")
        else:
            return topic

class MiscForm(forms.ModelForm):
    class Meta:
        model = Misc
        fields = ('task_name',)

    def clean_task_name(self):
        task_name = self.cleaned_data.get('task_name')
        if Misc.objects.filter(task_name__exact= task_name):
            raise forms.ValidationError("This task name is already existed")
        else:
            return task_name

class CustomForm(forms.ModelForm):
    class Meta:
        model = Custom
        fields = ()

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Custom.objects.filter(name__exact=name):
            raise forms.ValidationError("Custom name is already existed")
        else:
            return name

class CustomTaskForm(forms.ModelForm):
    class Meta:
        model = CustomTask
        fields = ('name',)

    def clean_name(self):
        name = self.objects.filter('name')
        if CustomTask.objects.filter(name__exact=name):
            raise forms.ValidationError("Custom task name is already existed")
        else:
            return name

class StudentEditForm(RegisterForm):
    class Meta():
        model = User
        fields = ['username', 'first_name', 'last_name']
