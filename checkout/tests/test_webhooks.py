"""
Test suite for the Stripe webhook entry point (webhooks.py).

Covers:
- Valid webhook events
- Invalid payload
- Invalid signature
- Fallback error handling
"""

from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.http import HttpResponse
from unittest.mock import patch, MagicMock
import json


@override_settings(STRIPE_WH_SECRET='whsec_test', STRIPE_SECRET_KEY='sk_test')
class WebhookViewTest(TestCase):
    """
    Tests for the webhook view handling Stripe events.
    """

    def setUp(self):
        self.client = Client()
        self.url = reverse('stripe_webhook')
        self.payload = json.dumps({
            "id": "evt_test_webhook",
            "type": "payment_intent.succeeded"
        }).encode('utf-8')
        self.sig_header = 't=12345,v1=abc,v0=xyz'

    @patch('stripe.Webhook.construct_event')
    @patch(
        'checkout.webhook_handler.StripeWH_Handler.handle_payment_intent_succeeded'
    )
    def test_valid_webhook_success(self, mock_handler, mock_construct):
        """
        Valid webhook with correct signature should call
        handler and return 200.
        """
        mock_construct.return_value = json.loads(self.payload)
        mock_handler.return_value = HttpResponse(status=200)

        response = self.client.post(
            self.url,
            data=self.payload,
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE=self.sig_header
        )
        self.assertEqual(response.status_code, 200)
        mock_handler.assert_called_once()

    @patch(
        'stripe.Webhook.construct_event',
        side_effect=ValueError("Invalid payload")
    )
    def test_invalid_payload_returns_400(self, mock_construct):
        """
        Webhook with invalid payload should return 400.
        """
        response = self.client.post(
            self.url,
            data=b'invalid-json',
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE=self.sig_header
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid payload', response.content)

    @patch('stripe.Webhook.construct_event')
    def test_signature_verification_error_returns_400(self, mock_construct):
        """
        Invalid signature should return 400.
        """
        from stripe.error import SignatureVerificationError
        mock_construct.side_effect = SignatureVerificationError(
            message="Bad signature", sig_header=self.sig_header
        )

        response = self.client.post(
            self.url,
            data=self.payload,
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE=self.sig_header
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid signature', response.content)

    @patch('stripe.Webhook.construct_event')
    def test_generic_exception_returns_400(self, mock_construct):
        """
        Generic unexpected error during event construction should return 400.
        """
        mock_construct.side_effect = Exception("Some other error")

        response = self.client.post(
            self.url,
            data=self.payload,
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE=self.sig_header
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Error: Some other error', response.content)
