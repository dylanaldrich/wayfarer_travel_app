from django.forms import ModelForm
from .models import Profile, Post
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

class Post_Form(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'city']

class Profile_Form(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'current_city', 'image']

class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=25)
    current_city = forms.CharField(max_length=25)
    email = forms.EmailField(max_length=150)

    class Meta:
        model = User
        fields = ('username', 'name', 'current_city', 'email', 'password1', 'password2',)

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
