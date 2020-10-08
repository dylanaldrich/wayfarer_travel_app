from django.forms import ModelForm
from .models import Profile, Post

class Post_Form(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']

class Profile_Form(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'current_city', 'image']