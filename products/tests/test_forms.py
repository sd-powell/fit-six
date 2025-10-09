from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from products.forms import ProductForm, ProductVariantForm
from products.models import Product, ProductVariant, Category


class ProductFormTest(TestCase):
    """
    Test suite for the ProductForm in the products app.

    Covers:
    - Valid form submission with and without an image
    - Dynamic category field population
    - Required fields and widget classes
    """

    def setUp(self):
        """
        Create a sample category for form use.
        """
        self.category = Category.objects.create(
            name='supplements', friendly_name='Supplements'
        )

    def test_product_form_valid_data(self):
        """
        Form should be valid when all required fields are filled.
        """
        form_data = {
            'name': 'Test Product',
            'description': 'Great product',
            'price': 10.00,
            'category': self.category.id,
        }
        form = ProductForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_product_form_invalid_without_required_fields(self):
        """
        Form should be invalid if required fields are missing.
        """
        form = ProductForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('description', form.errors)

    def test_product_form_category_friendly_names(self):
        """
        Category field choices should use friendly names.
        """
        form = ProductForm()
        choices = form.fields['category'].choices
        self.assertIn(
            (self.category.id, self.category.get_friendly_name()), choices
        )

    def test_product_form_widget_class_applied(self):
        """
        All form fields should have the expected CSS class.
        """
        form = ProductForm()
        for field in form.fields.values():
            self.assertIn('border-black', field.widget.attrs['class'])

    def test_product_form_image_optional(self):
        """
        Image upload should be optional and handled by custom widget.
        """
        form = ProductForm()
        image_field = form.fields['image']
        self.assertFalse(image_field.required)
        self.assertEqual(
            image_field.widget.__class__.__name__, 'CustomClearableFileInput'
        )


class ProductVariantFormTest(TestCase):
    """
    Test suite for the ProductVariantForm in the products app.

    Covers:
    - Basic field validation
    """

    def setUp(self):
        """
        Create a product for variant association.
        """
        self.category = Category.objects.create(
            name='test',
            friendly_name='Test'
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            category=self.category,
        )

    def test_variant_form_valid(self):
        """
        Form should validate with correct data.
        """
        form_data = {
            'size': 'M',
            'colour': 'Blue',
            'price': 9.99,
            'stock': 10
        }
        form = ProductVariantForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_variant_form_missing_fields(self):
        """
        Form should be invalid if required fields are missing.
        (In this model, 'price' and 'stock' are required.)
        """
        # Missing price
        form_data = {
            'size': 'M',
            'colour': 'Blue',
            # 'price' missing
            'stock': 10,
        }
        form = ProductVariantForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)

        # Missing stock
        form_data = {
            'size': 'L',
            'colour': 'Red',
            'price': 19.99,
            # 'stock' missing
        }
        form = ProductVariantForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('stock', form.errors)
