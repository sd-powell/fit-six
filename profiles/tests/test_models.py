from django.test import TestCase
from django.contrib.auth.models import User
from django_countries.fields import Country

from profiles.models import UserProfile


class UserProfileModelTest(TestCase):
    """
    Test suite for the UserProfile model.

    These tests verify:
    - Automatic creation of UserProfile via post_save signal.
    - Default values for fields are correctly set.
    - Updating field values persists as expected.
    - String representation returns the username.
    - Signal also updates profile on existing User save.
    """

    def setUp(self):
        """
        Create a User instance for use across tests.
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )

    def test_userprofile_created_on_user_creation(self):
        """
        Ensure a UserProfile is created automatically
        when a User instance is created.
        """
        profile = UserProfile.objects.get(user=self.user)
        self.assertIsInstance(profile, UserProfile)
        self.assertEqual(profile.user.username, 'testuser')

    def test_userprofile_str_method(self):
        """
        Test that the __str__ method of UserProfile
        returns the associated username.
        """
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(str(profile), 'testuser')

    def test_userprofile_default_values(self):
        """
        Test that default field values in the profile are
        correctly set to None or False.
        """
        profile = UserProfile.objects.get(user=self.user)
        self.assertFalse(profile.is_member)
        self.assertIsNone(profile.default_phone_number)
        self.assertIsNone(profile.default_street_address1)
        self.assertIsNone(profile.default_postcode)
        self.assertEqual(profile.default_country.code, None)

    def test_userprofile_field_update(self):
        """
        Test that field updates on the profile persist correctly.
        """
        profile = UserProfile.objects.get(user=self.user)
        profile.is_member = True
        profile.default_phone_number = '01234567890'
        profile.default_country = 'GB'
        profile.save()

        updated_profile = UserProfile.objects.get(user=self.user)
        self.assertTrue(updated_profile.is_member)
        self.assertEqual(updated_profile.default_phone_number, '01234567890')
        self.assertEqual(updated_profile.default_country, Country(code='GB'))

    def test_userprofile_updated_on_user_save(self):
        """
        Confirm that the post_save signal correctly triggers
        the UserProfile save when a User is updated.

        This test ensures no errors occur and the signal runs,
        not that unrelated profile fields are modified.
        """
        profile = UserProfile.objects.get(user=self.user)
        profile.default_phone_number = '555'
        profile.save()

        # Trigger the signal by updating the user
        self.user.first_name = 'UpdatedName'
        self.user.save()

        # Confirm the profile still exists and was saved
        updated_profile = UserProfile.objects.get(user=self.user)
        self.assertIsNotNone(updated_profile)
        self.assertEqual(updated_profile.user.first_name, 'UpdatedName')
