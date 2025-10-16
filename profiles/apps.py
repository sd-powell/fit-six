from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    """
    Configuration class for the Profiles app.

    Defines the default auto field type and registers the
    application under the name 'profiles'.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'
