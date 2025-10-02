from django.db import models
from django.utils import timezone
from profiles.models import UserProfile


class NewsletterSignup(models.Model):
    """
    Stores a single newsletter signup entry.

    This model captures the email address of a user who has opted in to receive
    marketing emails or newsletters. It optionally links the signup to a
    registered UserProfile, allowing tracking of signups by logged-in users.

    Attributes:
        user_profile (ForeignKey): Optional link to a UserProfile. Null if the
            signup was made anonymously.
        email (EmailField): The email address submitted during signup.
            Must be unique.
        date_joined (DateTimeField): The timestamp when the signup occurred.
    """
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='newsletter_signups'
    )
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.user_profile:
            return f"{self.user_profile.user.username} – {self.email}"
        return self.email
