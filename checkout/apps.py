"""
App configuration for the checkout app.
"""
from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    """Configuration for the Checkout app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout'

    def ready(self):
        """Import signal handlers when the app is ready."""
        import checkout.signals  # noqa: F401
