from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """
    Configuration class for the Products app.
    Sets the default auto field and registers the app name.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
