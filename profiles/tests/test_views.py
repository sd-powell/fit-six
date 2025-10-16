"""
Test suite for views in the profiles app.

Covers:
- Profile page accessibility for logged-in users
- Redirect for anonymous users
- Profile form update logic and messages
- Display of order history
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class ProfileViewTest(TestCase):
    """
    Test the profile view for login, update, and redirect behavior.
    """

    def setUp(self):
        """
        Create test user and associated profile.
        """
        self.user = User.objects.create_user(
            username='profileuser',
            password='securepassword',
            email='profile@example.com'
        )
        self.profile = self.user.userprofile

    def test_profile_redirect_if_not_logged_in(self):
        """
        Anonymous users should be redirected to login page.
        """
        response = self.client.get(reverse('profile'))
        self.assertRedirects(
            response,
            f"/accounts/login/?next={reverse('profile')}"
        )

    def test_profile_view_renders_for_logged_in_user(self):
        """
        Authenticated users should access the profile page successfully.
        """
        self.client.login(username='profileuser', password='securepassword')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')
        self.assertContains(response, 'Profile')

    def test_profile_update_form_submission(self):
        """
        Submitting updated profile data should save changes
        and display a success message.
        """
        self.client.login(username='profileuser', password='securepassword')
        update_data = {
            'default_phone_number': '1234567890',
            'default_street_address1': '123 Main St',
            'default_town_or_city': 'Testville',
            'default_postcode': 'AB12 3CD',
            'default_country': 'GB',
        }
        response = self.client.post(
            reverse('profile'), update_data, follow=True
        )
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.default_phone_number, '1234567890')

        messages = list(response.context['messages'])
        self.assertTrue(
            any("Profile updated successfully" in str(m) for m in messages)
        )

    def test_profile_update_invalid_form(self):
        """
        Submitting an invalid form (e.g., invalid country code)
        should return an error and not save changes.
        """
        self.client.login(username='profileuser', password='securepassword')
        response = self.client.post(reverse('profile'), {
            'default_country': 'INVALID'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

        self.profile.refresh_from_db()
        self.assertNotEqual(self.profile.default_country.code, 'INVALID')

        form = response.context['form']
        self.assertTrue(form.errors)

    def test_profile_post_invalid_form_shows_error_message(self):
        """
        Invalid profile submission should not save and should
        show error message.
        """
        self.client.login(username='profileuser', password='securepassword')

        invalid_data = {
            'default_phone_number': 'x' * 500,  # Too long, max_length=20
            'default_country': 'INVALID'       # Not a valid ISO code
        }

        response = self.client.post(
            reverse('profile'), invalid_data, follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

        # Form should be invalid
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('default_phone_number', form.errors)
        self.assertIn('default_country', form.errors)

        # Force check for the exact message from the view
        messages = list(response.context['messages'])
        self.assertTrue(
            any(
                'update failed. please ensure the form is valid'
                in str(m).lower()
                for m in messages
            ),
            "Expected 'Update failed...' message not found in response."
        )

    def test_profile_orders_displayed(self):
        """
        Ensure that the profile page includes the user's past orders.
        """
        self.client.login(username='profileuser', password='securepassword')

        from checkout.models import Order
        order = Order.objects.create(
            user_profile=self.profile,
            full_name='Test User',
            email='profile@example.com',
            phone_number='1234567890',
            country='GB',
            postcode='AB12 3CD',
            town_or_city='Testville',
            street_address1='123 Main St',
            street_address2='',
            county='',
            stripe_pid='test_pid',
            grand_total=10.00,
        )

        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')
        self.assertContains(response, order.order_number)

    def test_invalid_profile_form_triggers_error_block(self):
        """
        Force invalid form submission to hit the 'else' block
        in profiles/views.py and display an error message.
        """
        self.client.login(username='profileuser', password='securepassword')

        # Deliberately invalid: phone number too long
        response = self.client.post(reverse('profile'), {
            'default_phone_number': '1' * 100  # exceeds max_length=20
        }, follow=True)

        # Should render the same page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

        # Form should be invalid
        form = response.context['form']
        self.assertIn('default_phone_number', form.errors)

        # Confirm the 'Update failed' message appears
        messages = list(response.context['messages'])
        self.assertTrue(
            any('update failed' in str(m).lower() for m in messages),
            "Expected 'Update failed' message not found."
        )
