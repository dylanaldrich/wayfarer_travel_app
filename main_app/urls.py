
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('api/', views.api, name='api'),

    # ACCOUNTS (COMPLETE)
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/login/', views.login_user, name='login'),
    path('accounts/logout/', views.logout_user, name='logout'),
    path('errors/', views.error_detail, name='errors'),

    # PROFILES
    path('profiles/', views.profiles_index, name='profiles_index'),
    path('profile/<slug:slug>/', views.profile_detail, name='profile_detail'),
    path('profile/<int:user_id>/edit/', views.profile_edit, name='profile_edit'),
    # path('profile/<int:user_id>/delete/', views.profile_delete, name='profile_delete'),

    # POSTS
    path('posts/', views.post_index, name='post_index'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/create', views.post_create, name='post_create'),
    path('post/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),

   # COMMENTS
    path('post/<int:post_id>/comments/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/comments/<int:comment_id>/edit', views.edit_comment, name='edit_comment'),
    path('post/<int:post_id>/comments/<int:comment_id>/delete', views.delete_comment, name='delete_comment'),


    # CITIES
    path('cities/', views.cities_index, name='cities_index'),
    path('cities/<slug:slug>', views.cities_show, name='cities_show'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
