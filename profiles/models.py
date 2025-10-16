from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField


class UserProfile(models.Model):
    """
    Stores user profile information linked to the Django User model.

    Includes default delivery details, order history access,
    and Fit Six membership status (for discounts and promotions).
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_member = models.BooleanField(
        default=False,
        help_text=(
            "Designates whether the user is a Fit Six member "
            "eligible for discounts."
        ),
    )

    default_phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True
        )
    default_street_address1 = models.CharField(
        max_length=80,
        null=True,
        blank=True
        )
    default_street_address2 = models.CharField(
        max_length=80,
        null=True,
        blank=True
        )
    default_town_or_city = models.CharField(
        max_length=40,
        null=True,
        blank=True
        )
    default_county = models.CharField(max_length=80, null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(
        blank_label='Country',
        null=True,
        blank=True
        )

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create or update a user profile on user save.

    - If the user is newly created, a profile is created automatically.
    - For existing users, the profile is saved on update.
    """
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()
