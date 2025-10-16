from django.test import TestCase
from django.contrib.auth.models import User
from profiles.forms import UserProfileForm


class UserProfileFormTest(TestCase):
    """
    Test suite for the UserProfileForm class.

    Tests cover:
    - Form validation with required fields.
    - Placeholder and class application in __init__ method.
    - Label removal and autofocus on first field.
    """

    def setUp(self):
        """
        Create a test user and profile instance.
        """
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = self.user.userprofile

    def test_valid_form_data(self):
        """
        Ensure the form is valid when all required fields are provided.
        """
        form_data = {
            'default_phone_number': '07700111222',
            'default_postcode': 'NP26',
            'default_town_or_city': 'Magor',
            'default_street_address1': '123 Street',
            'default_street_address2': '',
            'default_county': 'Monmouthshire',
            'default_country': 'GB',
        }
        form = UserProfileForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())

    def test_form_field_placeholders_and_classes(self):
        """
        Check that each form field (excluding 'default_country') has:
        - A placeholder set
        - A CSS class applied
        - No label rendered
        """
        form = UserProfileForm(instance=self.profile)
        for name, field in form.fields.items():
            if name != 'default_country':
                self.assertIn('placeholder', field.widget.attrs)
                self.assertIn('border-black', field.widget.attrs['class'])
                self.assertFalse(field.label)

    def test_autofocus_set_on_phone_number(self):
        """
        Confirm the 'autofocus' attribute is set on the phone number field.
        """
        form = UserProfileForm(instance=self.profile)
        phone_attrs = form.fields['default_phone_number'].widget.attrs
        self.assertTrue(phone_attrs.get('autofocus'))
