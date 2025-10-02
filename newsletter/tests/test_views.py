from django.test import TestCase, RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from django.urls import reverse
from newsletter.models import NewsletterSignup
from newsletter.views import newsletter_signup


class NewsletterSignupViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.referer = '/some-page/'
        self.url = reverse('newsletter_signup')

    def _add_messages_middleware(self, request):
        """
        Attach the messages framework to a test request.

        Pattern based on Django documentation for simulating
        middleware behavior in unit tests.
        """
        setattr(request, 'session', self.client.session)
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

    def test_successful_signup(self):
        """
        Test that a valid signup email is saved and redirects with success.

        Follows the Django test client pattern for POST requests,
        with guidance from Django testing docs and community examples
        for request factory and message framework simulation.
        """
        request = self.factory.post(self.url, {'email': 'test@example.com'})
        request.META['HTTP_REFERER'] = self.referer
        self._add_messages_middleware(request)

        response = newsletter_signup(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.referer)
        self.assertTrue(
            NewsletterSignup.objects.filter(
                email='test@example.com'
            ).exists()
        )

    def test_duplicate_email_signup(self):
        """
        Test that submitting an already-subscribed email
        does not create a duplicate entry.

        Uses standard model setup and POST simulation techniques,
        as seen in Django model/view testing tutorials.
        """
        NewsletterSignup.objects.create(email='dupe@example.com')

        request = self.factory.post(
            self.url, {'email': 'dupe@example.com'})
        request.META['HTTP_REFERER'] = self.referer
        self._add_messages_middleware(request)

        response = newsletter_signup(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.referer)
        self.assertEqual(
            NewsletterSignup.objects.filter(
                email='dupe@example.com'
            ).count(), 1
        )

    def test_invalid_email_format(self):
        """
        Test that an invalid email address format is rejected.

        Informed by Django form validation techniques and
        message framework testing patterns.
        """
        request = self.factory.post(self.url, {'email': 'notanemail'})
        request.META['HTTP_REFERER'] = self.referer
        self._add_messages_middleware(request)

        response = newsletter_signup(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.referer)
        self.assertFalse(
            NewsletterSignup.objects.filter(
                email='notanemail'
            ).exists()
        )
