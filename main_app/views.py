from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Profile, Post, User
from .forms import Post_Form, Profile_Form, SignUpForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
# Base views
def home(request):
    signup_form = SignUpForm(request.POST)
    if signup_form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.profile.name = signup_form.cleaned_data.get('name')
        user.profile.current_city = signup_form.cleaned_data.get('current_city')
        user.profile.email = signup_form.cleaned_data.get('email')
        user.save()
        username = signup_form.cleaned_data.get('username')
        password = signup_form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    else:
        signup_form = SignUpForm()
    return render(request, 'home.html', {'signup_form': signup_form})


def about(request):
    return render(request, 'about.html')

def api(request):
    return JsonResponse({"status": 200})

# ----- Profile views -----

# Profile detail
def profiles_index(request):
    return HttpResponse('Hello, these are profiles')


# Profile Show
def profile_detail(request, user_id):
    profile = Profile.objects.get(user_id=user_id)
    context = {'profile': profile}
    return render(request, 'profiles/detail.html', context)


#Profile Edit
def profile_edit(request, user_id):
    profile = Profile.objects.get(id=user_id)
    if request.user == profile.user:
        if request.method == 'POST':
            profile_form = Profile_Form(request.POST, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('profiles/detail.html', user_id=user_id)
        else:
            profile_form = Profile_Form(instance=profile)
        context = {'profile': profile, 'profile_form': profile_form}
        return render(request, 'profiles/detail.html', context)
    return redirect('home')



# ------ Post views ------

# Posts Create
def post_create(request):
    if request.method == 'POST':
        post_form = Post_Form(request.POST)
        if post_form.is_valid():
            # save(commit=False) will just make a copy/instance of the model
            new_post = post_form.save(commit=False)
            new_post.user = request.user
            # save() to the db
            new_post.save()
            return redirect('posts/index.html')
    posts = Post.objects.filter(user=request.user)
    post_form = Post_Form()
    context = {'posts': posts, 'post_form': post_form}
    return render(request, 'posts/index.html', context)


# Posts Index
def post_index(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'posts/index.html', context)


# Post Show
def post_detail(request, post_id):
    post = Post.object.get(id=post_id)
    context = {'post': post}
    return render(request, 'posts/show.html', context)


# Post Edit && Update
def post_edit(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user == post.user:
        if request.method == 'POST':
            post_form = Post_Form(request.POST, instance=post)
            if post_form.is_valid():
                post_form.save()
                return redirect('posts/show.html', post_id=post_id)
        else:
            post_form = Post_Form(instance=post)
        context = {'post': post, 'post_form': post_form}
        return render(request, 'posts/show.html', context)
    return redirect('posts/show.html')

# Post Delete
def post_delete(request, post_id):
  post = Post.objects.get(id=post_id)
  if post.user == request.user:
    Post.objects.get(id=post_id).delete()
    return redirect("posts_index")
  return redirect("posts_index")


# ------ City views ------- #





# ------- User Auth -------#

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
        return redirect('profile_detail', user_id=user.id)
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# Login
def login_user(request):
    if request.method == 'POST':
        username_form = request.POST['username']
        password_form = request.POST['password']
        # authenticate user
        user = authenticate(username=username_form, password=password_form)
        if user is not None:
            # login
            login(request, user)
            #redirect
            return redirect('profile_detail', user_id=request.user.id)
        else:
            context = {'error':'Invalid Credentials'}
        return render(request, 'registration/login.html', context)
    else:
        return render(request, 'registration/login.html')

# Logout
def logout_user(request):
    logout(request)
    return redirect('home')


