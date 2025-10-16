from django.contrib import admin
from .models import NewsletterSignup


@admin.register(NewsletterSignup)
class NewsletterSignupAdmin(admin.ModelAdmin):
    """
    Admin configuration for the NewsletterSignup model.

    Registers the model in the Django admin panel with customized
    list display and search functionality for easy management
    of newsletter subscribers.
    """
    list_display = ('email', 'user_profile', 'date_joined')
    search_fields = ('email',)
