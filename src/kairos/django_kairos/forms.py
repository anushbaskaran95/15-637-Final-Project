from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


# Register Form
class RegisterForm(UserCreationForm):

    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'id': 'email'}))

    first_name = forms.CharField(label='First Name',
                                 widget=forms.TextInput(attrs={'id': 'first_name'}),
                                 max_length=50)

    last_name = forms.CharField(label='Last Name',
                                widget=forms.TextInput(attrs={'id': 'last_name'}),
                                max_length=50)

    class Meta:
        model = User
        exclude = ['username']
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        return cleaned_data

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
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        password = self.cleaned_data.get('password')

        new_user = User.objects.create_user(username=None,
                                            email=email,
                                            first_name=first_name,
                                            last_name=last_name,
                                            password=password)
        new_user.save()

        return new_user