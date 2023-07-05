from django import forms
from .models import Ticket, Review, UserFollows


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['ticket', 'rating', 'headline', 'body']


class FollowForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ['followed_user']
