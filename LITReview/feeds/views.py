from django.shortcuts import render
from datetime import datetime
from django.contrib.auth.models import User
from .models import Ticket, Review, UserFollows
from .forms import TicketForm, ReviewForm, FollowForm
from django.contrib.auth.decorators import login_required


@login_required(login_url='user-login')
def index(request, *args, **kwargs):
    tickets = Ticket.objects.order_by('-time_created')
    reviews = Review.objects.order_by('-time_created')
    if request.method == "POST":
        ticket_form = TicketForm(request.POST or None)
        review_form = ReviewForm(request.POST or None)
        if Ticket.DoesNotExist:
            pass
        else:
            ticket_id = int(request.POST['ticket'])
            review_form.instance.ticket = Ticket.objects.get(pk=ticket_id)
        if ticket_form.is_valid():
            ticket_to_save = ticket_form.save(commit=False)
            ticket_to_save.user = request.user
            ticket_to_save.time_created = datetime.now()
            ticket_form.save()
        if review_form.is_valid():
            review_to_save = review_form.save(commit=False)
            review_to_save.user = request.user
            review_to_save.time_created = datetime.now()
            review_form.save()
        return render(request, "index.html", {'tickets': tickets, 'reviews': reviews})
    else:
        return render(request, "index.html", {'tickets': tickets, 'reviews': reviews})


@login_required(login_url='user-login')
def created_tickets(request, *args, **kwargs):
    tickets = Ticket.objects.order_by('-time_created')
    reviews = Review.objects.order_by('-time_created')
    tickets_count = 0
    for ticket in tickets:
        if ticket.user == request.user:
            tickets_count += 1
    if request.method == "POST":
        ticket_form = TicketForm(request.POST or None)
        review_form = ReviewForm(request.POST or None)
        if Ticket.DoesNotExist:
            pass
        else:
            ticket_id = int(request.POST['ticket'])
            review_form.instance.ticket = Ticket.objects.get(pk=ticket_id)
        if ticket_form.is_valid():
            ticket_to_save = ticket_form.save(commit=False)
            ticket_to_save.user = request.user
            ticket_to_save.time_created = datetime.now()
            ticket_form.save()
        if review_form.is_valid():
            review_to_save = review_form.save(commit=False)
            review_to_save.user = request.user
            review_to_save.time_created = datetime.now()
            review_form.save()
        return render(request, "created_tickets.html", {'tickets': tickets, 'reviews': reviews,
                                                        'tickets_count': tickets_count})
    else:
        return render(request, "created_tickets.html", {'tickets': tickets, 'reviews': reviews,
                                                        'tickets_count': tickets_count})


def submitted_reviews(request, *args, **kwargs):
    tickets = Ticket.objects.order_by('-time_created')
    reviews = Review.objects.order_by('-time_created')
    reviewed_tickets = []
    for ticket in tickets:
        for review in reviews:
            if review.ticket == ticket and review.user == request.user:
                reviewed_tickets.append(ticket)
    for reviewed_ticket in reviewed_tickets:
        while reviewed_tickets.count(reviewed_ticket) > 1:
            reviewed_tickets.remove(reviewed_ticket)
    return render(request, "submitted_reviews.html", {'tickets': tickets, 'reviews': reviews,
                                                      'reviewed_tickets': reviewed_tickets})


@login_required(login_url='user-login')
def manage_follows(request, *args, **kwargs):
    user_follows = UserFollows.objects.order_by('-pk')
    followings_count = 0
    followers_count = 0
    for follow in user_follows:
        if follow.user == request.user:
            followings_count += 1
        elif follow.followed_user == request.user:
            followers_count += 1
    if request.method == "POST":
        follow_form = FollowForm(request.POST or None)
        followeduser = str(request.POST['followeduser'])
        follow_form.instance.followed_user = User.objects.get(username=followeduser)
        if not follow_form.is_valid():
            followeduser2 = User.objects.get(username=followeduser)
            UserFollows.objects.create(user=request.user, followed_user=followeduser2)
        else:
            follow_to_save = follow_form.save(commit=False)
            follow_to_save.user = request.user
            follow_form.save()
        return render(request, "manage_follows.html", {'user_follows': user_follows,
                                                       'followings_count': followings_count,
                                                       'followers_count': followers_count})
    else:
        return render(request, "manage_follows.html", {'user_follows': user_follows,
                                                       'followings_count': followings_count,
                                                       'followers_count': followers_count})


def register(request, *args, **kwargs):
    return render(request, "user/register.html")
