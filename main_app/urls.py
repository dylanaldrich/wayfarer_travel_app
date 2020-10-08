from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/login/', views.login_user, name='login'),
    path('accounts/logout/', views.logout_user, name='logout'),
    path('about/', views.about, name='about'),
    path('api/', views.api, name='api'),
    path('profiles/', views.profiles_index, name='profiles_index'),
    path('accounts/profile/<int:user_id>/', views.profile_detail, name='profile_detail'),
]
