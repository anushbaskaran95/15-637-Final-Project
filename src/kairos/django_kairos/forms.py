from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

from datetime import datetime, timedelta


# Login Form
class LoginForm(forms.Form):
    username = forms.CharField(label='username',
                               widget=forms.TextInput(attrs={'id': 'username'}),
                               max_length=20)

    password = forms.CharField(label='password',
                               widget=forms.PasswordInput(attrs={'id': 'password'}))

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username__exact=username):
            raise forms.ValidationError("Invalid Username")
        else:
            return username

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if len(User.objects.filter(username__exact=username)) == 1:
            user = User.objects.get(username__exact=username)
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect Password for "+username)
            else:
                return password
        else:
            return password


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
        if Course.objects.filter(course_name__iexact=course_name):
            raise forms.ValidationError("Course already exists")
        else:
            return course_name


class TaskInfoForm(forms.ModelForm):

    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'Start Date'},
                                                        format='%d %B, %Y'))
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'timepicker', 'placeholder': 'Start Time'},
                                                        format='%H:%M'))
    expected_finish_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker',
                                                                         'placeholder': 'Expected Finish Date'},
                                                                  format='%d %B, %Y'))
    expected_finish_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'timepicker',
                                                                         'placeholder': 'Expected Finish Time'},
                                                                  format='%H:%M'))
    due_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'Due Date'},
                                                      format='%d %B, %Y'), required=False)
    due_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'timepicker', 'placeholder': 'Due Time'},
                                                      format='%H:%M'), required=False)

    class Meta:
        model = TaskInfo
        exclude = ('date_paused', 'time_paused', 'status',)

    # def clean_start_time(self):
    #     start_time = self.cleaned_data.get('start_time')
    #     if start_time < datetime.now():
    #         raise forms.ValidationError("Invalid start time")
    #     else:
    #         return start_time
    #
    # def clean_expected_finish_time(self):
    #     expected_finish_time = self.cleaned_data.get('expected_finish_time')
    #     start_time = self.cleaned_data.get('start_time')
    #     if expected_finish_time <= start_time:
    #         raise forms.ValidationError("Expected finish time should be after start time")
    #     else:
    #         return expected_finish_time
    #
    # def clean_due_date(self):
    #     due_date = self.cleaned_data.get('due_date')
    #     start_time = self.cleaned_data.get('start_time')
    #     if due_date <= start_time:
    #         raise forms.ValidationError("Due date should be after start time")
    #     else:
    #         return due_date

    def clean_percentage_completion(self):
        percentage_completion = self.cleaned_data.get('percentage_completion')
        if percentage_completion < 0 or percentage_completion > 100:
            forms.ValidationError("Invalid percentage completion")
        else:
            return percentage_completion


class CourseTaskForm(forms.ModelForm):
    class Meta:
        model = CourseTask
        fields = ('name',)

    def clean(self):
        cleaned_data = super(CourseTaskForm, self).clean()
        return cleaned_data


class ResearchForm(forms.ModelForm):
    class Meta:
        model = Research
        fields = ('topic',)

    def clean_topic(self):
        topic = self.cleaned_data.get('topic')
        if Research.objects.filter(topic__iexact=topic):
            raise forms.ValidationError("This research topic already exists")
        else:
            return topic


class MiscForm(forms.ModelForm):
    class Meta:
        model = Misc
        fields = ('task_name',)

    def clean(self):
        cleaned_data = super(MiscForm, self).clean()
        return cleaned_data


class StudentEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super(StudentEditForm, self).clean()
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username already exists")
        else:
            return username
