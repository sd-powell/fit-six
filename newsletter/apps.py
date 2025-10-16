from django.apps import AppConfig


class NewsletterConfig(AppConfig):
    """
    App configuration for the Newsletter app.

    Defines the default auto field and app name used by Django
    to register and manage the newsletter application.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "newsletter"
