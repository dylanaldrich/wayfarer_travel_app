from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Profile, Post
from .forms import Post_Form, Profile_Form, SignUpForm
from django.contrib.auth import login, authenticate
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

# ----- Profile views -----

# Profile detail
def profile_detail(request, user_id):
    profile = Profile.objects.filter(user_id=user_id)
    context = {'profile': profile}
    return render(request, 'profiles/detail.html', context)

# Post views
# Posts index
# def post_index(request):
#     posts = Post.objects.all()
#     context = {'posts': posts}
#     return render(request, 'posts/index.html', context)

# City views

# Signup
def signup(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.profile.name = form.cleaned_data.get('name')
        user.profile.current_city = form.cleaned_data.get('current_city')
        user.profile.email = form.cleaned_data.get('email')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('profile_detail')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
