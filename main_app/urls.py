
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('api/', views.api, name='api'),

    # ACCOUNTS (COMPLETE)
    path('accounts/signup/', views.signup, name='signup'), # COMPLETE
    path('accounts/login/', views.login_user, name='login'), # COMPLETE
    path('accounts/logout/', views.logout_user, name='logout'), # COMPLETE

    # PROFILES
    path('profiles/', views.profiles_index, name='profiles_index'), # WAIT SPRINT 2
    path('profile/<int:user_id>/', views.profile_detail, name='profile_detail'), # COMPLETE
    path('profile/<int:user_id>/edit/', views.profile_edit, name='profile_edit'), # DYLAN TODO -- OPENS TO A NEW PAGE
    # path('profile/<int:user_id>/delete/', views.profile_delete, name='profile_delete'),

    # POSTS
    path('posts/', views.post_index, name='post_index'), # WAIT SPRINT 2
    path('post/<int:post_id>/', views.post_detail, name='post_detail'), # BEATRIX TODO -- OPENS TO A NEW PAGE
    path('posts/create', views.post_create, name='post_create'), # LIA TODO -- WILL BE MODAL in the futurreeeeee
    path('post/<int:post_id>/edit/', views.post_edit, name='post_edit'), # WAIT SPRINT 2
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'), # WAIT SPRINT 2

    # CITIES
    path('cities/', views.cities_index, name='cities_index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
