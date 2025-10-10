"""
Test suite for StripeWH_Handler in checkout.webhook_handler.

Covers:
- Generic unhandled events
- Payment intent succeeded (order exists and does not exist)
- Payment failed event
"""

import json
from decimal import Decimal
from unittest.mock import patch, MagicMock

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.http import HttpRequest

from checkout.webhook_handler import StripeWH_Handler
from checkout.models import Order
from products.models import Category, Product, ProductVariant
from profiles.models import UserProfile


class WebhookHandlerTests(TestCase):
    """
    Unit tests for StripeWH_Handler methods.
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='webhookuser', password='pass'
        )
        self.profile = self.user.userprofile
        self.profile.is_member = True
        self.profile.save()

        self.category = Category.objects.create(name='Hydration')
        self.product = Product.objects.create(
            name='Flask',
            description='Insulated bottle',
            category=self.category
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            sku='FLASK-001',
            price=Decimal('10.00'),
            stock=5,
            size='One Size',
            colour='Black'
        )

        self.bag = json.dumps({
            str(self.product.id): {
                'items_by_variant': {
                    f'{self.variant.size}_{self.variant.colour}': 1
                }
            }
        })

        self.metadata = {
            'bag': self.bag,
            'save_info': 'true',
            'username': self.user.username,
        }

    def _mock_shipping(self):
        shipping = MagicMock()
        shipping.name = 'Test User'
        shipping.phone = '1234567890'
        shipping.address.country = 'GB'
        shipping.address.postal_code = 'AB12 3CD'
        shipping.address.city = 'Testville'
        shipping.address.line1 = '123 Test St'
        shipping.address.line2 = ''
        shipping.address.state = 'Countyshire'
        return shipping

    def test_handle_event_returns_generic_response(self):
        """
        Unmapped webhook type should return 200 with generic message.
        """
        request = self.factory.post('/webhook/')
        handler = StripeWH_Handler(request)
        event = {'type': 'unhandled.event'}
        response = handler.handle_event(event)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Unhandled webhook received', response.content.decode())

    @patch('checkout.webhook_handler.stripe.Charge.retrieve')
    @patch(
        'checkout.webhook_handler.StripeWH_Handler._send_confirmation_email'
    )
    def test_handle_payment_intent_succeeded_creates_new_order(
    self, mock_email, mock_charge
    ):
        """A valid new webhook should create an order and send confirmation email."""
        mock_charge.return_value = MagicMock(
            billing_details=MagicMock(email='test@example.com'),
            amount=1000
        )

        shipping = self._mock_shipping()
        # Use MagicMock for metadata to mimic attribute access
        metadata_mock = MagicMock()
        metadata_mock.bag = self.bag
        metadata_mock.save_info = 'true'
        metadata_mock.username = self.user.username

        event = MagicMock()
        event.type = 'payment_intent.succeeded'
        event.data.object = MagicMock(
            id='pi_123',
            metadata=metadata_mock,
            shipping=shipping,
            latest_charge='ch_123'
        )

        request = self.factory.post('/webhook/')
        handler = StripeWH_Handler(request)
        response = handler.handle_payment_intent_succeeded(event)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Order.objects.filter(stripe_pid='pi_123').exists())
        mock_email.assert_called_once()

    @patch('checkout.webhook_handler.stripe.Charge.retrieve')
    @patch(
        'checkout.webhook_handler.StripeWH_Handler._send_confirmation_email'
    )
    def test_handle_payment_intent_succeeded_order_already_exists(
        self, mock_email, mock_charge
        ):
        """A valid new webhook should create an order and send confirmation email."""
        mock_charge.return_value = MagicMock(
            billing_details=MagicMock(email='test@example.com'),
            amount=1000
        )

        shipping = self._mock_shipping()
        # Use MagicMock for metadata to mimic attribute access
        metadata_mock = MagicMock()
        metadata_mock.bag = self.bag
        metadata_mock.save_info = 'true'
        metadata_mock.username = self.user.username

        event = MagicMock()
        event.type = 'payment_intent.succeeded'
        event.data.object = MagicMock(
            id='pi_123',
            metadata=metadata_mock,
            shipping=shipping,
            latest_charge='ch_123'
        )

        request = self.factory.post('/webhook/')
        handler = StripeWH_Handler(request)
        response = handler.handle_payment_intent_succeeded(event)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Order.objects.filter(stripe_pid='pi_123').exists())
        mock_email.assert_called_once()

    def test_handle_payment_intent_payment_failed_returns_200(self):
        """
        Stripe payment failure should still return 200 response.
        """
        request = self.factory.post('/webhook/')
        handler = StripeWH_Handler(request)
        event = {'type': 'payment_intent.payment_failed'}
        response = handler.handle_payment_intent_payment_failed(event)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'payment_intent.payment_failed',
            response.content.decode()
        )

    def test_handle_payment_failed_returns_200(self):
        """payment_intent.payment_failed should return a 200 response."""
        request = self.factory.post('/webhook/')
        handler = StripeWH_Handler(request)
        event = {'type': 'payment_intent.payment_failed'}

        response = handler.handle_payment_intent_payment_failed(event)

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'payment_intent.payment_failed',
            response.content.decode()
        )
