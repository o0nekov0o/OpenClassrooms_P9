from django.shortcuts import render
from datetime import datetime
from .models import Ticket, Review
from .forms import TicketForm, ReviewForm
from django.contrib.auth.decorators import login_required


@login_required(login_url='user-login')
def index(request, *args, **kwargs):
    tickets = Ticket.objects.order_by('-time_created')
    reviews = Review.objects.order_by('-time_created')
    if request.method == "POST":
        ticket_form = TicketForm(request.POST or None)
        review_form = ReviewForm(request.POST or None)
        ticket_id = int(request.POST['ticket'])
        review_form.instance.ticket = Ticket.objects.get(id=ticket_id)
        if ticket_form.is_valid():
            ticket_to_save = ticket_form.save(commit=False)
            ticket_to_save.user = request.user
            ticket_to_save.time_created = datetime.now()
            ticket_form.save()
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.time_created = datetime.now()
            review_form.save()
        return render(request, "index.html", {'tickets': tickets, 'reviews': reviews})
    else:
        return render(request, "index.html", {'tickets': tickets, 'reviews': reviews})


@login_required(login_url='user-login')
def created_tickets(request, *args, **kwargs):
    tickets = Ticket.objects.order_by('-time_created')
    reviews = Review.objects.order_by('-time_created')
    return render(request, "created_tickets.html", {'tickets': tickets, 'reviews': reviews})


def register(request, *args, **kwargs):
    return render(request, "user/register.html")
