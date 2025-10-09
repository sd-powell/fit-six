from django.test import TestCase
from django.contrib.auth.models import User
from django_countries.fields import Country

from profiles.models import UserProfile


class UserProfileModelTest(TestCase):
    """
    Test suite for the UserProfile model.

    These tests verify:
    - Automatic profile creation via signal when a new User is created.
    - String representation (__str__ method).
    - Field default values and update functionality.
    """

    def setUp(self):
        """
        Create a user for use in all tests.
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            first_name='Test',
            last_name='User',
        )

    def test_userprofile_created_on_user_creation(self):
        """
        Ensure a UserProfile is created automatically
        when a new User is created.
        """
        profile = UserProfile.objects.get(user=self.user)
        self.assertIsInstance(profile, UserProfile)
        self.assertEqual(profile.user.username, 'testuser')

    def test_userprofile_str_returns_username(self):
        """
        Test the string representation of the
        UserProfile model returns the username.
        """
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(str(profile), 'testuser')

    def test_userprofile_default_field_values(self):
        """
        Verify that default values of profile fields
        are set to None, False, or blank as expected.
        """
        profile = UserProfile.objects.get(user=self.user)
        self.assertFalse(profile.is_member)
        self.assertIsNone(profile.default_phone_number)
        self.assertIsNone(profile.default_street_address1)
        self.assertIsNone(profile.default_postcode)

        # CountryField returns Country(code=None), not None — use assertFalse
        self.assertFalse(profile.default_country)

    def test_userprofile_field_update(self):
        """
        Update fields in the UserProfile and verify they persist correctly.
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
