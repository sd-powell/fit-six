"""
Test suite for the Product, ProductVariant, and Category models.

This module covers:
- String representations of each model.
- Relationships between Product and Category.
- Relationship and output formatting of ProductVariant.
"""

from decimal import Decimal
from django.test import TestCase
from products.models import Category, Product, ProductVariant


class CategoryModelTest(TestCase):
    """
    Tests for the Category model.
    """

    def setUp(self):
        self.category = Category.objects.create(
            name='apparel',
            friendly_name='Apparel & Clothing'
        )

    def test_str_returns_name(self):
        """
        __str__ should return the category's name.
        """
        self.assertEqual(str(self.category), 'apparel')

    def test_get_friendly_name(self):
        """
        get_friendly_name() should return the friendly name.
        """
        self.assertEqual(
            self.category.get_friendly_name(),
            'Apparel & Clothing'
        )


class ProductModelTest(TestCase):
    """
    Tests for the Product model.
    """

    def setUp(self):
        self.category = Category.objects.create(name='accessories')
        self.product = Product.objects.create(
            name='Water Bottle',
            description='Insulated bottle',
            category=self.category,
            has_variants=True,
        )

    def test_str_returns_name(self):
        """
        __str__ should return the product's name.
        """
        self.assertEqual(str(self.product), 'Water Bottle')

    def test_product_category_relationship(self):
        """
        Product should be linked to the correct category.
        """
        self.assertEqual(self.product.category.name, 'accessories')


class ProductVariantModelTest(TestCase):
    """
    Tests for the ProductVariant model.
    """

    def setUp(self):
        self.product = Product.objects.create(
            name='T-Shirt',
            description='Cotton shirt',
            has_variants=True
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            sku='TSHIRT-BLUE-M',
            price=Decimal('19.99'),
            stock=10,
            size='M',
            colour='Blue'
        )

    def test_str_returns_formatted_variant(self):
        """
        __str__ should return a string with product name, size, and colour.
        """
        expected = 'T-Shirt - M - Blue'
        self.assertEqual(str(self.variant), expected)

    def test_defaults_for_optional_fields(self):
        """
        Optional fields like image and back image should default to None.
        """
        self.assertFalse(self.variant.image)
        self.assertFalse(self.variant.image_back)
