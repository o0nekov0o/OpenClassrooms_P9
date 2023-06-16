from django.shortcuts import render
from .forms import ReviewForm
from datetime import datetime
from .models import Ticket, Review
from django.contrib.auth.decorators import login_required


@login_required(login_url='user-login')
def index(request, *args, **kwargs):
    tickets = Ticket.objects.order_by('-time_created')
    reviews = Review.objects.all()
    if request.method == "POST":
        form = ReviewForm(request.POST or None)
        ticket_id = int(request.POST['ticket'])
        form.instance.ticket = Ticket.objects.get(id=ticket_id)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.time_created = datetime.now()
            form.save()
        else:
            print(form.instance.ticket)
            print(form.errors)
            print(form.non_field_errors())
        return render(request, "index.html", {'tickets': tickets, 'reviews': reviews})
    else:
        return render(request, "index.html", {'tickets': tickets, 'reviews': reviews})


def register(request, *args, **kwargs):
    return render(request, "user/register.html")
