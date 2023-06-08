from django.contrib import admin
from .models import Ticket, Review, UserFollows


class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user', 'image', 'time_created',)
    list_filter = ('title',)
    search_fields = ['title', 'description']


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'rating', 'headline', 'body', 'user', 'time_created',)
    list_filter = ('ticket',)
    search_fields = ['ticket', 'rating']


class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ('user', 'followed_user')
    list_filter = ('user',)
    search_fields = ['user', 'followed_user']


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserFollows, UserFollowsAdmin)
