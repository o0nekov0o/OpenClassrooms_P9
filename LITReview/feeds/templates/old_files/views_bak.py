import online_users.models
from django.shortcuts import render
from django.shortcuts import redirect
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from LITReview.feeds.models import Ticket, Review, UserFollows
from django.contrib.auth.decorators import login_required
from LITReview.feeds.forms import TicketForm, ReviewForm, FollowForm, RegisterForm


def post_method(request):
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


@login_required(login_url='user-login')
def index(request, *args, **kwargs):
    tickets = Ticket.objects.order_by('-pk')
    reviews = Review.objects.order_by('-pk')
    if request.method == "POST":
        post_method(request)
        return render(request, "index.html", {'tickets': tickets, 'reviews': reviews,
                                              'ticket_form': TicketForm()})
    else:
        return render(request, "index.html", {'tickets': tickets, 'reviews': reviews,
                                              'ticket_form': TicketForm()})


@login_required(login_url='user-login')
def created_tickets(request, *args, **kwargs):
    tickets = Ticket.objects.filter(user=request.user).order_by('-pk')
    reviews = Review.objects.order_by('-pk')
    if request.method == "POST":
        post_method(request)
        return render(request, "created_posts.html", {'tickets': tickets, 'reviews': reviews,
                                                        'ticket_form': TicketForm()})
    else:
        return render(request, "created_posts.html", {'tickets': tickets, 'reviews': reviews,
                                                        'ticket_form': TicketForm()})


@login_required(login_url='user-login')
def submitted_reviews(request, *args, **kwargs):
    reviews = Review.objects.filter(user=request.user).order_by('-pk')
    tickets = Ticket.objects.filter(review__in=reviews).order_by('-pk').distinct()
    return render(request, "submitted_reviews.html", {'tickets': tickets, 'reviews': reviews,
                                                      'ticket_form': TicketForm()})


@login_required(login_url='user-login')
def manage_follows(request, *args, **kwargs):
    followed_extract = UserFollows.objects.filter(user=request.user).values_list('followed_user_id', flat=True)
    followed_users = User.objects.filter(pk__in=followed_extract).all()
    subbed_extract = UserFollows.objects.filter(followed_user=request.user).values_list('user_id', flat=True)
    subbed_users = User.objects.filter(pk__in=subbed_extract).all()
    if request.method == "POST":
        follow_form = FollowForm(request.POST or None)
        followed_user = str(request.POST['followed_extract'])
        if follow_form.is_valid():
            follow_to_save = follow_form.save(commit=False)
            follow_to_save.followed_user = User.objects.get(username=followed_user)
            follow_to_save.user = request.user
            follow_form.save()
        else:
            print(follow_form.errors.as_data())
        return render(request, "manage_follows.html", {'followed_users': followed_users,
                                                       'subbed_users': subbed_users})
    else:
        return render(request, "manage_follows.html", {'followed_users': followed_users,
                                                       'subbed_users': subbed_users})


@login_required(login_url='user-login')
def follows_tickets(request, *args, **kwargs):
    followed_users = UserFollows.objects.filter(user=request.user).values_list('followed_user_id', flat=True)
    tickets = Ticket.objects.filter(user__pk__in=followed_users).order_by('-pk')
    reviews = Review.objects.order_by('-pk')
    return render(request, "follows_posts.html", {'tickets': tickets, 'reviews': reviews})


@login_required(login_url='user-login')
def follows_reviews(request, *args, **kwargs):
    followed_users = UserFollows.objects.filter(user=request.user).values_list('followed_user_id', flat=True)
    reviews = Review.objects.filter(user__pk__in=followed_users).order_by('-pk')
    tickets = Ticket.objects.filter(review__in=reviews).order_by('-pk').distinct()
    return render(request, "follows_reviews.html", {'tickets': tickets, 'reviews': reviews})


@login_required(login_url='user-login')
def online_follows(request, *args, **kwargs):
    user_activity_objects = online_users.models.OnlineUserActivity.get_user_activities(timedelta(seconds=60))
    connected_users = (user for user in user_activity_objects)
    followed_extract = UserFollows.objects.filter(user=request.user).values_list('followed_user_id', flat=True)
    connected_follows = User.objects.filter(onlineuseractivity__in=connected_users, pk__in=followed_extract)
    followed_users = User.objects.filter(pk__in=followed_extract).all()
    if request.method == "POST":
        unfollow_form = FollowForm(request.POST or None)
        unfollowed_extract = str(request.POST['unfollowed_user'])
        if unfollow_form.is_valid():
            unfollowed_user = User.objects.get(username=unfollowed_extract)
            UserFollows.objects.get(user=request.user, followed_user=unfollowed_user).delete()
        return render(request, "online_follows.html", {'connected_follows': connected_follows,
                                                       'followed_users': followed_users})
    else:
        return render(request, "online_follows.html", {'connected_follows': connected_follows,
                                                       'followed_users': followed_users})


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


@login_required
def edit_ticket(request, *args, **kwargs):
    if request.method == 'POST':
        ticket_id = int(request.POST['ticket'])
        ticket = Ticket.objects.get(pk=ticket_id)
        ticket_form = TicketForm(request.POST, request.FILES, instance=ticket)
        if not ticket_form.is_valid():
            ticket_form = TicketForm(instance=ticket)
            return render(request, 'edit_ticket.html', {'ticket_form': ticket_form, 'ticket': ticket})
        if ticket_form.is_valid():
            ticket_form.time_created = datetime.now()
            ticket_form.save()
            return redirect(index)
    else:
        return redirect(index)
    
      
@login_required
def edit_review(request, *args, **kwargs):
    if request.method == 'POST':
        review_id = int(request.POST['review'])
        review = Ticket.objects.get(pk=review_id)
        review_form = ReviewForm(request.POST, instance=review)
        if not review_form.is_valid():
            review_form = ReviewForm(instance=review)
            return render(request, 'edit_review.html', {'review_form': review_form, 'review': review})
        if review_form.is_valid():
            review_form.time_created = datetime.now()
            review_form.save()
            return redirect(index)
    else:
        return redirect(index)


@login_required
def delete_ticket(request, *args, **kwargs):
    if request.method == 'POST':
        ticket_id = int(request.POST['ticket'])
        ticket = Ticket.objects.get(pk=ticket_id)
        ticket_form = TicketForm(request.POST, request.FILES, instance=ticket)
        if not ticket_form.is_valid():
            ticket_form = TicketForm(instance=ticket)
            return render(request, 'delete_ticket.html', {'ticket_form': ticket_form, 'ticket': ticket})
    elif request.method == 'GET':
        if Ticket.DoesNotExist:
            return redirect(index)
        ticket_id = int(request.GET['ticket'])
        ticket = Ticket.objects.get(pk=ticket_id)
        ticket_form = TicketForm(request.GET, request.FILES, instance=ticket)
        if not ticket_form.is_valid():
            ticket.delete()
            return redirect(index)
    else:
        return redirect(index)


def create_ticket(request, *args, **kwargs):
    return render(request, "create_ticket.html", {'ticket_form': TicketForm()})


def profile(request, *args, **kwargs):
    return render(request, "user/profile.html")


def profile_update(request, *args, **kwargs):
    return render(request, "user/profile_update.html")
