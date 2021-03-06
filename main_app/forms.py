from django.forms import ModelForm
from .models import Profile, Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django import forms
from captcha.fields import CaptchaField
from crispy_forms.helper import FormHelper

class Post_Form(ModelForm):
    title = forms.CharField(max_length= 200, required=True)

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
    captcha = CaptchaField()

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

    class Meta:
        model = User
        fields = ('username', 'name', 'current_city', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))

class Comment_Form(ModelForm):
        class Meta:
            model = Comment
            fields = ['comment']
