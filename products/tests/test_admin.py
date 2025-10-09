"""
Test suite for the custom admin configuration of the Product app.

Covers:
- Model registration in the admin site
- Admin display configuration for Product and ProductVariant
- Fieldsets, search fields, and ordering
"""

from django.test import TestCase, RequestFactory
from django.contrib.admin.sites import site
from products.models import Product, ProductVariant, Category
from products.admin import ProductAdmin, ProductVariantAdmin, CategoryAdmin
from products.admin import ProductVariantInline


class ProductAdminTest(TestCase):
    """
    Tests for ProductAdmin configuration.
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.category = Category.objects.create(name='gear')
        self.product = Product.objects.create(
            name='Hat',
            description='Sun hat',
            category=self.category,
            has_variants=True
        )

    def test_model_registered(self):
        """Check Product model is registered in the admin site."""
        self.assertIn(Product, site._registry)

    def test_product_admin_list_display(self):
        """Ensure 'name' and 'category' are in list_display."""
        ma = ProductAdmin(Product, site)
        self.assertIn('name', ma.list_display)
        self.assertIn('category', ma.list_display)

    def test_product_admin_search_fields(self):
        """Ensure search_fields is configured properly."""
        ma = ProductAdmin(Product, site)
        self.assertIn('name', ma.search_fields)

    def test_product_admin_ordering(self):
        """Ensure default ordering is by name."""
        ma = ProductAdmin(Product, site)
        self.assertEqual(ma.ordering, ('name',))

    def test_product_admin_readonly_fields(self):
        """Ensure 'image_preview' is a readonly field in ProductAdmin."""
        ma = ProductAdmin(Product, site)
        self.assertIn('image_preview', ma.readonly_fields)

    def test_product_admin_fields(self):
        """Ensure expected fields appear in the ProductAdmin form."""
        ma = ProductAdmin(Product, site)
        self.assertIn('name', [f for f in ma.fields])
        self.assertIn('image_preview', ma.fields)

    def test_product_admin_inline(self):
        """Ensure ProductVariantInline is used in ProductAdmin."""
        ma = ProductAdmin(Product, site)
        self.assertIn(ProductVariantInline, ma.inlines)

    def test_image_preview_returns_img_tag(self):
        """Ensure image_preview returns <img> tag when image is present."""
        self.product.image = 'media/sample.jpg'  # simulate image path
        ma = ProductAdmin(Product, site)
        result = ma.image_preview(self.product)
        self.assertIn('<img', result)
        self.assertIn('sample.jpg', result)

    def test_image_preview_returns_placeholder_when_no_image(self):
        """Ensure image_preview returns fallback text when image is missing."""
        self.product.image = None
        ma = ProductAdmin(Product, site)
        result = ma.image_preview(self.product)
        self.assertEqual(result, '(No image)')


class ProductVariantAdminTest(TestCase):
    """
    Tests for ProductVariantAdmin configuration.
    """

    def setUp(self):
        self.product = Product.objects.create(
            name='Bag',
            description='Backpack',
            has_variants=True
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            sku='BAG123',
            price=19.99,
            stock=10,
            size='M',
            colour='Black'
        )

    def test_model_registered(self):
        """Check ProductVariant model is registered in the admin site."""
        self.assertIn(ProductVariant, site._registry)

    def test_variant_admin_list_display_fields(self):
        """
        Ensure all expected fields appear in ProductVariantAdmin list_display.
        """
        ma = ProductVariantAdmin(ProductVariant, site)
        expected_fields = [
            'sku',
            'product',
            'price',
            'stock',
            'size',
            'colour',
            'variant_image_preview',
            'variant_back_image_preview',
        ]
        for field in expected_fields:
            self.assertIn(field, ma.list_display)

    def test_variant_admin_readonly_fields(self):
        """Ensure preview fields are readonly in ProductVariantAdmin."""
        ma = ProductVariantAdmin(ProductVariant, site)
        self.assertIn('variant_image_preview', ma.readonly_fields)
        self.assertIn('variant_back_image_preview', ma.readonly_fields)

    def test_variant_image_preview_with_image(self):
        """Ensure variant_image_preview returns
        an image tag if image exists."""
        self.variant.image = 'media/front.jpg'
        ma = ProductVariantAdmin(ProductVariant, site)
        result = ma.variant_image_preview(self.variant)
        self.assertIn('<img', result)
        self.assertIn('front.jpg', result)

    def test_variant_image_preview_without_image(self):
        """Ensure variant_image_preview returns placeholder
        if no image exists."""
        self.variant.image = None
        ma = ProductVariantAdmin(ProductVariant, site)
        result = ma.variant_image_preview(self.variant)
        self.assertEqual(result, '(No image)')

    def test_variant_back_image_preview_with_image(self):
        """Ensure variant_back_image_preview returns image
        tag if image exists."""
        self.variant.image_back = 'media/back.jpg'
        ma = ProductVariantAdmin(ProductVariant, site)
        result = ma.variant_back_image_preview(self.variant)
        self.assertIn('<img', result)
        self.assertIn('back.jpg', result)

    def test_variant_back_image_preview_without_image(self):
        """Ensure variant_back_image_preview returns placeholder
        if no image exists."""
        self.variant.image_back = None
        ma = ProductVariantAdmin(ProductVariant, site)
        result = ma.variant_back_image_preview(self.variant)
        self.assertEqual(result, '(No back image)')


class CategoryAdminTest(TestCase):
    """
    Tests for CategoryAdmin configuration.
    """

    def setUp(self):
        self.category = Category.objects.create(
            name='accessories',
            friendly_name='Accessories'
        )

    def test_model_registered(self):
        """Check Category model is registered in the admin site."""
        self.assertIn(Category, site._registry)

    def test_category_admin_list_display(self):
        """Check list_display includes name and friendly_name."""
        ma = CategoryAdmin(Category, site)
        self.assertEqual(ma.list_display, ('friendly_name', 'name'))


class ProductVariantInlineTest(TestCase):
    """
    Tests for preview methods in ProductVariantInline.
    """

    def setUp(self):
        self.product = Product.objects.create(
            name='Bottle',
            description='Stainless steel',
            has_variants=True
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            sku='BOTTLE001',
            price=12.50,
            stock=5,
            size='L',
            colour='Silver'
        )
        self.inline = ProductVariantInline(self.variant, site)

    def test_preview_with_image(self):
        """Return <img> tag if image exists."""
        self.variant.image = 'media/preview.jpg'
        result = self.inline.preview(self.variant)
        self.assertIn('<img', result)

    def test_preview_without_image(self):
        """Return fallback text if image is missing."""
        self.variant.image = None
        result = self.inline.preview(self.variant)
        self.assertEqual(result, '(No image)')

    def test_preview_back_with_image(self):
        """Return <img> tag if back image exists."""
        self.variant.image_back = 'media/back-preview.jpg'
        result = self.inline.preview_back(self.variant)
        self.assertIn('<img', result)

    def test_preview_back_without_image(self):
        """Return fallback text if back image is missing."""
        self.variant.image_back = None
        result = self.inline.preview_back(self.variant)
        self.assertEqual(result, '(No back image)')
