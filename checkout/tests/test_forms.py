"""
Test suite for checkout models: Order and OrderLineItem.

Covers:
- String representations
- Total and delivery cost calculations
"""

from decimal import Decimal
from django.test import TestCase
from checkout.models import Order, OrderLineItem
from django.contrib.auth.models import User
from products.models import Product, ProductVariant, Category


class OrderModelTest(TestCase):
    """
    Tests for Order model logic and output.
    """

    def setUp(self):
        user = User.objects.create_user(username='testuser2', password='pass')
        self.profile = user.userprofile
        self.category = Category.objects.create(name='accessories')
        self.product = Product.objects.create(
            name='Cap',
            description='A snapback cap',
            category=self.category,
            has_variants=False
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            sku='CAP-002',
            price=19.99,
            stock=5,
            size='One Size',
            colour='Black'
        )
        self.order = Order.objects.create(
            user_profile=self.profile,
            full_name='User Two',
            email='user2@example.com',
            phone_number='0123456789',
            street_address1='456 Road',
            town_or_city='City',
            postcode='CD34 5EF',
            country='GB',
            stripe_pid='pid456',
        )
        self.lineitem = OrderLineItem.objects.create(
            order=self.order,
            variant=self.variant,
            quantity=2,
            lineitem_total=39.98
        )

    def test_order_str_returns_order_number(self):
        """__str__ should return the order number."""
        self.assertEqual(str(self.order), self.order.order_number)

    def test_update_total_adds_correct_totals(self):
        """update_total should calculate lineitems + delivery correctly."""
        self.order.update_total()
        self.assertEqual(self.order.order_total, Decimal('39.98'))
        self.assertEqual(
            self.order.grand_total,
            self.order.order_total + self.order.delivery_cost
        )


class OrderLineItemModelTest(TestCase):
    """
    Tests for OrderLineItem logic.
    """

    def setUp(self):
        user = User.objects.create_user(username='testuser2', password='pass')
        self.profile = user.userprofile
        self.category = Category.objects.create(name='accessories')
        self.product = Product.objects.create(
            name='Cap',
            description='A snapback cap',
            category=self.category,
            has_variants=False
        )

        self.variant = ProductVariant.objects.create(
            product=self.product,
            sku='CAP-003',
            price=19.99,
            stock=5,
            size='One Size',
            colour='Black'
        )

        self.order = Order.objects.create(
            user_profile=self.profile,
            full_name='User Two',
            email='user2@example.com',
            phone_number='0123456789',
            street_address1='456 Road',
            town_or_city='City',
            postcode='CD34 5EF',
            country='GB',
            stripe_pid='pid456',
        )
        self.lineitem = OrderLineItem.objects.create(
            order=self.order,
            variant=self.variant,
            quantity=2,
            lineitem_total=39.98
        )

    def test_order_line_item_str(self):
        """__str__ should return a readable description of the line item."""
        expected = f'SKU {self.variant.sku} on order {self.order.order_number}'
        self.assertEqual(str(self.lineitem), expected)
