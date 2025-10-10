"""
Test suite for OrderForm in the checkout app.

Covers:
- Placeholder text rendering
- Field label suppression
- Autofocus attribute
- CSS class application
"""

from django.test import TestCase
from checkout.forms import OrderForm


class OrderFormTest(TestCase):
    """
    Tests for the custom behaviour of the OrderForm.
    """

    def setUp(self):
        self.form = OrderForm()

    def test_field_placeholders_and_classes(self):
        """
        Each field should have the correct placeholder and CSS class.
        'country' should not have a placeholder.
        """
        expected_placeholders = {
            'full_name': 'Full Name *',
            'email': 'Email Address *',
            'phone_number': 'Phone Number *',
            'street_address1': 'Street Address 1 *',
            'street_address2': 'Street Address 2',
            'town_or_city': 'Town or City *',
            'postcode': 'Postal Code',
            'county': 'County, State or Locality',
        }

        for field_name, expected_placeholder in expected_placeholders.items():
            field = self.form.fields[field_name]
            self.assertEqual(
                field.widget.attrs.get('placeholder'),
                expected_placeholder,
                f"Placeholder mismatch for {field_name}"
            )
            self.assertEqual(
                field.widget.attrs.get('class'),
                'stripe-style-input',
                f"Missing or incorrect CSS class for {field_name}"
            )

        # Country should not have a placeholder but should have the class
        country_field = self.form.fields['country']
        self.assertNotIn('placeholder', country_field.widget.attrs)
        self.assertEqual(
            country_field.widget.attrs.get('class'),
            'stripe-style-input',
            "Missing CSS class for country field"
        )

    def test_field_labels_are_suppressed(self):
        """
        All form fields should have label set to False.
        """
        for name, field in self.form.fields.items():
            self.assertFalse(field.label, f"Label not suppressed for {name}")

    def test_full_name_has_autofocus(self):
        """
        full_name field should have autofocus enabled.
        """
        autofocus = (
            self.form.fields['full_name'].widget.attrs.get('autofocus', False)
        )
        self.assertTrue(autofocus, "Autofocus not set on full_name field")
