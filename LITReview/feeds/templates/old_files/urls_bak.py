"""LITReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from feeds.views import index, register, created_tickets, manage_follows, submitted_reviews, \
    follows_tickets, follows_reviews, online_follows, edit_ticket, edit_review, delete_ticket, \
    delete_review, create_ticket, profile, profile_update

urlpatterns = [
    path("", index, name='index'),
    path('admin/', admin.site.urls),
    path('profile/', profile, name='user-profile'),
    path('register/', register, name='user-register'),
    path('edit_ticket/', edit_ticket, name='edit_ticket'),
    path('edit_review/', edit_review, name='edit_review'),
    path('create_ticket/', create_ticket, name='create_ticket'),
    path('delete_ticket/', delete_ticket, name='delete_ticket'),
    path('delete_review/', delete_review, name='delete_review'),
    path("manage_follows/", manage_follows, name='manage_follows'),
    path("online_follows/", online_follows, name='online_follows'),
    path("follows_tickets/", follows_tickets, name='follows_tickets'),
    path('follows_reviews/', follows_reviews, name='follows_reviews'),
    path("created_tickets/", created_tickets, name='created_tickets'),
    path('profile_update/', profile_update, name='user-profile-update'),
    path("submitted_reviews/", submitted_reviews, name='submitted_reviews'),
    path('login/', LoginView.as_view(template_name='user/login.html'), name='user-login'),
    path('logout/', LogoutView.as_view(template_name='user/logout.html'), name='user-logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
