from django.forms import ModelForm
from .models import Profile, Post
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class Post_Form(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']

class Profile_Form(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'current_city']


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=150, help_text='Email')
    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2',)