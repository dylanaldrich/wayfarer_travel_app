from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('about/', views.about, name='about'),
    path('api/', views.api, name='api'),
    path('posts_index/', views.post_index, name='post_index')
]
