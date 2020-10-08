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
    name = forms.CharField(max_length=25)
    current_city = forms.CharField(max_length=25)
    email = forms.EmailField(max_length=150)

    class Meta:
        model = User
        fields = ('username', 'name', 'current_city', 'email', 'password1', 'password2',)

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))

#     def clean(self, *args, **kwargs):
#         username = self.cleaned_data.get("username")
#         password = self.cleaned_data.get("password")

#         if username and password:
#             user = authenticate(username=username, password=password)
#             if not user:
#                 raise forms.ValidationError("This user does not exist")
#             if not user.check_password(password):
#                 raise forms.ValidationError("Incorrect password")
#             if not user.is_active:
#                 raise forms.ValidationError("This user is no longer active")
#             return super(UserLoginForm, self).clean(*args, **kwargs)
