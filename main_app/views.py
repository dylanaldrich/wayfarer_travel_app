from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Profile, Post, User, City
from .forms import Post_Form, Profile_Form, SignUpForm, LoginForm, Post_Form
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q


# Create your views here.
# Base views
def home(request):
    signup_form = SignUpForm(data=request.POST)
    if signup_form.is_valid():
        user = signup_form.save()
        user.refresh_from_db()
        user.profile.name = signup_form.cleaned_data.get('name')
        user.profile.current_city = signup_form.cleaned_data.get('current_city')
        user.profile.email = signup_form.cleaned_data.get('email')
        user.save()
        username = signup_form.cleaned_data.get('username')
        password = signup_form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        mail_subject = 'Welcome to Wayfarer'
        message = render_to_string('registration/welcome_email.html', {
                'user': user,})
        to_email = signup_form.cleaned_data.get('email')
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        login(request, user)
        return redirect('profile_detail', slug=user.profile.slug)
    else:
        context={
            'errors': signup_form.errors,
            'signup_form': SignUpForm(),
        }
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')

def api(request):
    return JsonResponse({"status": 200})

# ----- Profile views -----

# Profiles index
def profiles_index(request):
    return HttpResponse('Hello, these are profiles')


# # Profile detail
def profile_detail(request, slug):
    profile = Profile.objects.get(slug=slug)
    form = Post_Form(request.POST)
    posts = Post.objects.filter(user_id=profile.id).values_list('city__name', flat=True)
    cities = Post.objects.filter(user_id=profile.id).values_list('city__name', flat=True).order_by('city__name').distinct('city__name')
    # cities = Post.objects.filter(user_id=profile.id, city__name='San Francisco').values_list('city__name', flat=True)
    # cities = Post.objects.filter(user_id=profile.id, city__name='San Francisco')
    context = {'profile': profile, 'form': form, 'cities': cities, 'posts': posts}
    return render(request, 'profiles/detail.html', context)


# def profile_detail(request, slug):
#     profile = Profile.objects.get(slug=slug)
#     form = Post_Form(request.POST)
#     posts = Post.objects.filter(user_id=profile.id)
#     post_cities = []
#     for post in posts:
#         post_cities.append(post.city.name)


#     def countFreq(arr, n):
#         distinct_post_cities = []
#         city_posts_count = []
#         # Mark all array elements as not visited
#         visited = [False for i in range(n)]

#         # Traverse through array elements and count frequencies
#         for i in range(n):
#             # Skip this element if already processed
#             if (visited[i] == True):
#                 continue

#             # Count frequency
#             count = 1
#             for j in range(i + 1, n, 1):
#                 if (arr[i] == arr[j]):
#                     visited[j] = True
#                     count += 1

#             distinct_post_cities.append(arr[i])
#             city_posts_count.append(count)
#         print('Distinct cities: ', distinct_post_cities)
#         print('post count per city:', city_posts_count)

#     countFreq(post_cities, len(post_cities))
#     context = {'profile': profile, 'form': form}
#     return render(request, 'profiles/detail.html', context)


# Profile Edit & Update
def profile_edit(request, user_id):
    profile = Profile.objects.get(id=user_id)
    print("REQUEST.FILES", request.FILES)
    if request.method == 'POST':
        try:
            profile_form = Profile_Form(request.POST, request.FILES, instance=profile)
            # profile_form = Profile_Form(request.POST, request.FILES, instance=user.profile)
            if profile_form.is_valid():
                new_profile = profile_form.save(commit=False)
                new_profile.user = request.user
                if request.FILES.get('image'):
                    new_profile.image = request.FILES['image']
                new_profile.save()
        except:
            profile_form = Profile_Form(request.POST, request.FILES)
            if profile_form.is_valid():
                new_profile = profile_form.save(commit=False)
                new_profile.user = request.user
                new_profile.image = request.FILES['image']
                new_profile.save()
        return redirect('profile_detail', slug=request.user.profile.slug)
    else:
        try:
            profile_form = Profile_Form(instance=profile)
            # profile_form = Profile_Form(instance=user.profile)
            context = {'profile_form': profile_form, 'profile': profile}
            return render(request, 'profiles/edit.html', context)
        except:
            profile_form = Profile_Form()
            context = {'profile_form': profile_form}
            return render(request, 'profiles/edit.html', context)


# ------ Post views ------

# Posts Create
def post_create(request):
    cities = City.objects.all()
    if request.method == 'POST':
        post_form = Post_Form(data=request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect('cities_index')
        else:
            return redirect('cities_index')
    posts = Post.objects.filter(user=request.user)
    post_form = Post_Form()
    context = {'posts': posts, 'post_form': post_form, 'cities': cities}
    return render(request, 'posts/create.html', context)


# Posts Index
def post_index(request):
    posts_list = Post.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(posts_list, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    cities = City.objects.all()
    form = Post_Form(request.POST)
    context = {'posts': posts, 'form': form, 'cities': cities}
    return render(request, 'posts/index.html', context)


# Post Show
def post_detail(request, post_id):
    posts = Post.objects.all()
    post = Post.objects.get(id=post_id)
    cities = City.objects.all()
    profile = Profile.objects.get(user_id=post.user_id)
    context = {'posts': posts, 'post': post, 'cities': cities, 'profile': profile}
    return render(request, 'posts/show.html', context)


# Post Edit && Update
def post_edit(request, post_id):
    post = Post.objects.get(id=post_id)
    cities = City.objects.all()
    if request.user == post.user:
        if request.method == 'POST':
            post_form = Post_Form(request.POST, instance=post)
            if post_form.is_valid():
                post_form.save()
                return redirect('post_detail', post_id=post_id)
        else:
            post_form = Post_Form(instance=post)
        context = {'post': post, 'post_form': post_form, 'cities': cities}
        return render(request, 'posts/edit.html', context)
    return redirect('post_index')

# Post Delete
def post_delete(request, post_id):
    post = Post.objects.get(id=post_id)
    print('request.user.id', request.user.id)
    if post.user == request.user:
        Post.objects.get(id=post_id).delete()
        return redirect('profile_detail', slug=request.user.profile.slug)


# ------ City views ------- #

# Cities Index
def cities_index(request):
    posts_list = Post.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(posts_list, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    cities = City.objects.all()
    form = Post_Form(request.POST)
    context = {'posts': posts, 'form': form, 'cities': cities}
    return render(request, 'cities/index.html', context)



# Cities Show
def cities_show(request, slug):
    cities = City.objects.all()
    city = City.objects.get(slug=slug)
    posts_list = Post.objects.filter(city=city.id)
    page = request.GET.get('page', 1)
    paginator = Paginator(posts_list, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    cities = City.objects.all()
    form = Post_Form(request.POST)
    context = {'cities': cities, 'city': city, 'form': form, 'posts': posts}
    return render(request, 'cities/show.html', context)

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
        mail_subject = 'Welcome to Wayfarer'
        message = render_to_string('registration/welcome_email.html', {
                'user': user,})
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(mail_subject, message, to=[to_email])
        # email.send()
        login(request, user)
        return redirect('profile_detail', slug=user.profile.slug)
    else:
        context={
            'errors': form.errors,
            'form': SignUpForm(),
        }
    return render(request, 'registration/signup.html', context)

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
            return redirect('profile_detail', slug=user.profile.slug)
        else:
            context = {'error':'Invalid Credentials - a true wanderer?'}
        return render(request, 'registration/login.html', context)
    else:
        return render(request, 'registration/login.html')


# Logout
def logout_user(request):
    logout(request)
    return redirect('home')
