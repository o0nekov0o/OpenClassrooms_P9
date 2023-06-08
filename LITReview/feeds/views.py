from django.shortcuts import render
from django.http import HttpResponse


def home(request, *args, **kwargs):
    return HttpResponse("<h1>Hey</h1>")
