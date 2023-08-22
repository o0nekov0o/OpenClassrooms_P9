import online_users.models
from django.db.models import Q
from django.shortcuts import render
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from .models import Ticket, Review, UserFollows
from django.contrib.auth.decorators import login_required
from .forms import TicketForm, ReviewForm, FollowForm, RegisterForm


@login_required(login_url='user-login')
def index(request, *args, **kwargs):
    tickets = Ticket.objects.order_by('-time_created')
    reviews = Review.objects.order_by('-time_created')
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES or None)
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
        return render(request, "index.html", {'tickets': tickets, 'reviews': reviews,
                                              'ticket_form': TicketForm()})
    else:
        return render(request, "index.html", {'tickets': tickets, 'reviews': reviews,
                                              'ticket_form': TicketForm()})


@login_required(login_url='user-login')
def created_tickets(request, *args, **kwargs):
    tickets = Ticket.objects.order_by('-time_created')
    reviews = Review.objects.order_by('-time_created')
    tickets_count = 0
    for ticket in tickets:
        if ticket.user == request.user:
            tickets_count += 1
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES or None)
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
        return render(request, "created_posts.html", {'tickets': tickets, 'reviews': reviews,
                                                        'tickets_count': tickets_count,
                                                        'ticket_form': TicketForm()})
    else:
        return render(request, "created_posts.html", {'tickets': tickets, 'reviews': reviews,
                                                        'tickets_count': tickets_count,
                                                        'ticket_form': TicketForm()})


@login_required(login_url='user-login')
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
        return render(request, "manage_follows.html", {'user_follows': user_follows,
                                                       'followings_count': followings_count,
                                                       'followers_count': followers_count})
    else:
        return render(request, "manage_follows.html", {'user_follows': user_follows,
                                                       'followings_count': followings_count,
                                                       'followers_count': followers_count})


@login_required(login_url='user-login')
def follows_tickets(request, *args, **kwargs):
    tickets = Ticket.objects.order_by('-time_created')
    reviews = Review.objects.order_by('-time_created')
    user_follows = UserFollows.objects.order_by('-pk')
    tickets_count = 0
    for follow in user_follows:
        for ticket in tickets:
            if follow.user == request.user and ticket.user == follow.followed_user:
                tickets_count += 1
    return render(request, "follows_posts.html", {'tickets': tickets, 'reviews': reviews,
                                                    'tickets_count': tickets_count,
                                                    'user_follows': user_follows})


@login_required(login_url='user-login')
def follows_reviews(request, *args, **kwargs):
    tickets = Ticket.objects.order_by('-time_created')
    reviews = Review.objects.order_by('-time_created')
    user_follows = UserFollows.objects.order_by('-pk')
    reviewed_tickets = []
    for ticket in tickets:
        for review in reviews:
            for follow in user_follows:
                if follow.user == request.user and review.ticket == ticket \
                        and review.user == follow.followed_user:
                    reviewed_tickets.append(ticket)
    for reviewed_ticket in reviewed_tickets:
        while reviewed_tickets.count(reviewed_ticket) > 1:
            reviewed_tickets.remove(reviewed_ticket)
    return render(request, "follows_reviews.html", {'tickets': tickets, 'reviews': reviews,
                                                    'reviewed_tickets': reviewed_tickets,
                                                    'user_follows': user_follows})


@login_required(login_url='user-login')
def online_follows(request, *args, **kwargs):
    user_activity_objects = online_users.models.OnlineUserActivity.get_user_activities(timedelta(seconds=60))
    connected_users = (user for user in user_activity_objects)
    user_follows = UserFollows.objects.order_by('-pk')
    connected_follows = []
    followings_count = 0
    for follow in user_follows:
        if follow.user == request.user:
            followings_count += 1
    for connected_user in connected_users:
        for follow in user_follows:
            if follow.user == request.user and follow.followed_user == connected_user.user:
                connected_follows.append(follow.followed_user)
    for connected_follow in connected_follows:
        while connected_follows.count(connected_follow) > 1:
            connected_follows.remove(connected_follow)
    if request.method == "POST":
        unfollow_form = FollowForm(request.POST or None)
        unfolloweduser = str(request.POST['unfolloweduser'])
        unfollow_form.instance.followed_user = User.objects.get(username=unfolloweduser)
        if not unfollow_form.is_valid():
            unfolloweduser2 = User.objects.get(username=unfolloweduser)
            UserFollows.objects.get(user=request.user, followed_user=unfolloweduser2).delete()
        return render(request, "online_follows.html", {'connected_follows': connected_follows,
                                                       'user_follows': user_follows,
                                                       'followings_count': followings_count})
    else:
        return render(request, "online_follows.html", {'connected_follows': connected_follows,
                                                       'user_follows': user_follows,
                                                       'followings_count': followings_count})


def register(request, *args, **kwargs):
    if request.method == "POST":
        register_form = RegisterForm(request.POST or None)
        email = str(request.POST['email'])
        users = User.objects.order_by('-pk')
        username = str(request.POST['username'])
        email_error = 'Please provide a different email that is not already in use. '
        username_error = 'Please provide a different username that is not already in use. '
        signup_success = 'Registration successful. Problem to connect ? Click ForgottenPassword. '
        for user in users:
            if user.email == email:
                return render(request, "user/register.html", {'email_error': email_error})
        for user in users:
            if user.username == username:
                return render(request, "user/register.html", {'username_error': username_error})
        if register_form.is_valid():
            register_to_confirm = register_form.save(commit=False)
            register_to_confirm.time_created = datetime.now()
            register_to_confirm.save()
            return render(request, "user/register.html", {'signup_success': signup_success})
    else:
        return render(request, "user/register.html")


def create_ticket(request, *args, **kwargs):
    return render(request, "create_ticket.html", {'ticket_form': TicketForm()})


def profile(request, *args, **kwargs):
    return render(request, "user/profile.html")


def profile_update(request, *args, **kwargs):
    return render(request, "user/profile_update.html")
