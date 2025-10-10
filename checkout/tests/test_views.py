"""
Test suite for views in the checkout app.

Covers:
- Checkout page rendering and form context
- Redirect on empty bag
- Checkout success page behavior
- Stripe cache endpoint behavior
"""

from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from checkout.models import Order
from profiles.models import UserProfile
from products.models import Product, ProductVariant, Category


class CheckoutViewsTest(TestCase):
    """
    Tests for checkout views: checkout, success, and cache.
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='checkoutuser',
            password='testpass'
        )
        self.category = Category.objects.create(name='gear')
        self.product = Product.objects.create(
            name='Bottle',
            description='Water bottle',
            category=self.category
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            sku='BOT-001',
            price=10.00,
            stock=5,
            size='One Size',
            colour='Blue'
        )
        self.client.session['bag'] = {
            str(self.product.id): {
                'items_by_variant': {
                    'One Size_Blue': 1
                }
            }
        }
        self.client.session.save()

    def test_checkout_get_view(self):
        """
        GET request to checkout should load form and stripe context.
        """
        self.client.login(username='checkoutuser', password='testpass')

        # Create a real priced variant
        self.category = Category.objects.create(name='test')
        self.product = Product.objects.create(
            name='T-Shirt',
            description='Cool shirt',
            category=self.category,
            has_variants=True
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            sku='TS-001',
            price=Decimal('10.00'),
            stock=10,
            size='M',
            colour='Blue'
        )

        # Add this priced item to the session bag
        session = self.client.session
        session['bag'] = {
            str(self.product.id): {
                'items_by_variant': {
                    f'{self.variant.size}_{self.variant.colour}': 1
                }
            }
        }
        session.save()

        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')
        self.assertIn('stripe_public_key', response.context)
        self.assertIn('order_form', response.context)

    def test_checkout_redirects_with_empty_bag(self):
        """
        If bag is empty, user should be redirected from checkout.
        """
        session = self.client.session
        session['bag'] = {}
        session.save()
        response = self.client.get(reverse('checkout'), follow=True)
        self.assertRedirects(response, reverse('products'))

    def test_checkout_success_view(self):
        """
        checkout_success view should show success message and clear bag.
        """
        self.client.login(username='checkoutuser', password='testpass')
        profile = UserProfile.objects.get(user=self.user)
        order = Order.objects.create(
            order_number='TEST123',
            user_profile=profile,
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            country='GB',
            street_address1='123 Main St',
            town_or_city='City',
            postcode='AB12 3CD',
            stripe_pid='testpid'
        )
        session = self.client.session
        session['save_info'] = True
        session['bag'] = {'some': 'thing'}
        session.save()

        response = self.client.get(
            reverse('checkout_success', args=['TEST123']), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        self.assertIn('order', response.context)
        self.assertNotIn('bag', self.client.session)

    def test_cache_checkout_data_view(self):
        """
        POST to cache_checkout_data should return 200 or 400.
        """
        self.client.login(username='checkoutuser', password='testpass')
        response = self.client.post(
            reverse('cache_checkout_data'),
            data={
                'client_secret': 'pi_12345_secret_abcde',
                'save_info': 'true'
            }
        )
        self.assertIn(response.status_code, [200, 400])

    def test_checkout_missing_variant_redirects(self):
        """
        If a variant in the bag does not exist, user is redirected with error.
        """
        self.client.login(username='checkoutuser', password='testpass')

        # Valid product ID, but invalid variant combination
        session = self.client.session
        session['bag'] = {
            str(self.product.id): {
                'items_by_variant': {
                    'FakeSize_FakeColour': 1  # This variant doesn't exist
                }
            }
        }
        session.save()

        response = self.client.post(reverse('checkout'), {
            'full_name': 'Name',
            'email': 'test@example.com',
            'phone_number': '123',
            'country': 'GB',
            'postcode': '123',
            'town_or_city': 'Town',
            'street_address1': '123 St',
            'street_address2': '',
            'county': '',
            'client_secret': 'pi_12345_secret_abcde'
        }, follow=True)

        self.assertRedirects(response, reverse('view_bag'))
        messages = list(response.context['messages'])
        self.assertTrue(any("wasn't found" in str(m) for m in messages))

    def test_checkout_invalid_form_shows_error(self):
        """
        Invalid form submission should show error message and re-render page.
        """
        self.client.login(username='checkoutuser', password='testpass')

        # Add valid product + variant to the bag
        session = self.client.session
        session['bag'] = {
            str(self.product.id): {
                'items_by_variant': {
                    f'{self.variant.size}_{self.variant.colour}': 1
                }
            }
        }
        session.save()

        response = self.client.post(reverse('checkout'), {
            'full_name': '',  # Invalid (required)
            'email': '',
            'phone_number': '',
            'country': '',
            'postcode': '',
            'town_or_city': '',
            'street_address1': '',
            'street_address2': '',
            'county': '',
            'client_secret': 'pi_12345_secret_abcde'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')
        self.assertContains(response, 'There was an error with your form')
