from django.test import TestCase
from newsletter.forms import NewsletterSignupForm
from newsletter.models import NewsletterSignup


class TestNewsletterSignupForm(TestCase):
    def test_valid_email_is_accepted(self):
        """Test that a new, valid email passes form validation.

        Based on standard Django form testing patterns
        learned from official docs and testing tutorials.
        """
        form_data = {'email': 'newuser@example.com'}
        form = NewsletterSignupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_duplicate_email_is_rejected(self):
        """Test that an already subscribed email
        raises a validation error.

        Pattern learned from testing custom `clean_email()` methods
        with pre-existing model data, as shown in community examples.
        """
        # First create an entry with the email
        NewsletterSignup.objects.create(email='test@example.com')

        form_data = {'email': 'test@example.com'}
        form = NewsletterSignupForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(
            form.errors['email'][0],
            "This email is already subscribed."
        )

    def test_email_is_lowercased(self):
        """Test that the form treats uppercase email
        as lowercase duplicates.

        Inspired by Django best practices for normalising input
        and enforcing uniqueness across case-insensitive email addresses.
        """
        NewsletterSignup.objects.create(email='hello@site.com')

        form_data = {'email': 'HELLO@SITE.COM'}
        form = NewsletterSignupForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(
            form.errors['email'][0],
            "This email is already subscribed."
        )
