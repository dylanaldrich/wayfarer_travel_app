from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('about/', views.about, name='about'),
    path('api/', views.api, name='api'),
    path('/profile/<int:user_id>/', views.profile_detail, name='profile_detail')
]
