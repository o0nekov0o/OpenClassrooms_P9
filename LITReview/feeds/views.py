from django.shortcuts import render
from .models import Ticket, Review
from django.contrib.auth.decorators import login_required


@login_required(login_url='user-login')
def index(request, *args, **kwargs):
    tickets = Ticket.objects.order_by('-time_created')
    reviews = Review.objects.all()
    return render(request, "index.html", {'tickets': tickets, 'reviews': reviews})


def register(request, *args, **kwargs):
    return render(request, "user/register.html")
