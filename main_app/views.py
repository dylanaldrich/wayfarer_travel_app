from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Profile, Post
from .forms import Post_Form, Profile_Form, SignUpForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.

# Base views
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def api(request):
    return JsonResponse({"status": 200})

# Profile views

# Post views
# Posts index
def post_index(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'posts/index.html', context)

# City views


# Signup
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
        profile = profile_form.save()
        login(request, user)
        return redirect('home')
    else:
        error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    profile_form = Profile_Form()
    context = {'form': form, 'profile_form':profile_form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)