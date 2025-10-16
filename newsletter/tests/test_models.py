from django.test import TestCase
from django.contrib.auth.models import User
from newsletter.models import NewsletterSignup


class NewsletterSignupModelTests(TestCase):
    def setUp(self):
        # Use a unique user instance for each test
        # Pattern based on Django's recommended test setup using fixtures
        self.user = User.objects.create_user(
            username='testuser1',
            email='testuser1@example.com',
            password='password123'
        )
        self.profile = self.user.userprofile

    def test_create_signup_with_user_profile(self):
        """
        Test creating a signup linked to a UserProfile.

        Follows standard model instance creation testing,
        learned from Django testing documentation and previous
        project patterns.
        """
        signup = NewsletterSignup.objects.create(
            user_profile=self.profile,
            email='userprofile@example.com'
        )
        self.assertEqual(signup.email, 'userprofile@example.com')
        self.assertEqual(signup.user_profile, self.profile)

    def test_create_signup_without_user_profile(self):
        """
        Test creating a signup without linking a user profile.

        Based on model testing examples where nullable fields are optional.
        """
        signup = NewsletterSignup.objects.create(
            email='anonymous@example.com'
        )
        self.assertEqual(signup.email, 'anonymous@example.com')
        self.assertIsNone(signup.user_profile)

    def test_email_uniqueness(self):
        """
        Test that the model enforces uniqueness of email.

        Common validation scenario derived from real-world examples
        where EmailField is set to unique=True in the model.
        """
        NewsletterSignup.objects.create(email='unique@example.com')
        with self.assertRaises(Exception):
            NewsletterSignup.objects.create(email='unique@example.com')

    def test_str_method_with_user_profile(self):
        """
        Test __str__ method output when a UserProfile is present.

        Inspired by Django best practices for model string representations.
        """
        signup = NewsletterSignup.objects.create(
            user_profile=self.profile,
            email='str@example.com'
        )
        expected_str = f"{self.user.username} – str@example.com"
        self.assertEqual(str(signup), expected_str)

    def test_str_method_without_user_profile(self):
        """
        Test __str__ method output when no UserProfile is linked.

        Patterned after examples in Django’s model testing tutorials.
        """
        signup = NewsletterSignup.objects.create(
            email='no-profile@example.com'
        )
        self.assertEqual(str(signup), 'no-profile@example.com')
