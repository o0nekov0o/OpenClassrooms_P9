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
from django.contrib.auth.views import LoginView, LogoutView
from feeds.views import index, register, created_tickets, manage_follows, submitted_reviews

urlpatterns = [
    path("", index, name='index'),
    path('admin/', admin.site.urls),
    path('register/', register, name='user-register'),
    path("manage_follows/", manage_follows, name='manage_follows'),
    path("created_tickets/", created_tickets, name='created_tickets'),
    path("submitted_reviews/", submitted_reviews, name='submitted_reviews'),
    path('login/', LoginView.as_view(template_name='user/login.html'), name='user-login'),
    path('logout/', LogoutView.as_view(template_name='user/logout.html'), name='user-logout'),
]
