from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


@login_required(login_url='user-login')
def index(request, *args, **kwargs):
    users = get_user_model().objects.all()
    return render(request, "index.html", {'users': users})


def register(request, *args, **kwargs):
    return render(request, "user/register.html")
