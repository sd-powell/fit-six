from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product, Category, ProductVariant


class ProductViewsTest(TestCase):
    """
    Test suite for product-related views including:
    - Listing, detail, search, and sorting
    - Add/edit/delete views (admin-only)
    """

    def setUp(self):
        """
        Create test user, category, product, and variant for use in views.
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.admin_user = User.objects.create_superuser(
            username='adminuser',
            password='adminpass'
        )
        self.category = Category.objects.create(
            name='tops',
            friendly_name='Tops'
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='A test product',
            category=self.category
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            size='M',
            colour='Red',
            price=20.00,
            stock=5
        )

    def test_all_products_view(self):
        """
        Verify that the all_products view returns a 200 response and uses
        the correct template.
        """
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_product_detail_view(self):
        """
        Verify the product_detail view returns 200 and correct context.
        """
        url = reverse('product_detail', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')
        self.assertContains(response, 'Test Product')

    def test_product_search_query(self):
        """
        Ensure product search query returns the expected product.
        """
        response = self.client.get(reverse('products'), {'q': 'test'})
        self.assertContains(response, 'Test Product')

    def test_empty_search_query_redirects(self):
        """
        Ensure empty search query redirects with error message.
        """
        response = self.client.get(reverse('products'), {'q': ''}, follow=True)
        self.assertRedirects(response, reverse('products'))
        messages = list(response.context['messages'])
        self.assertTrue(
            any("didn't enter any search criteria" in str(m) for m in messages)
        )

    def test_product_sorting(self):
        """
        Ensure product sorting does not throw errors.
        """
        response = self.client.get(reverse('products'), {'sort': 'name'})
        self.assertEqual(response.status_code, 200)

    def test_product_sorting_by_price(self):
        """
        Ensure products can be sorted by price.
        """
        response = self.client.get(reverse('products'), {
            'sort': 'price',
            'direction': 'asc'
        })
        self.assertEqual(response.status_code, 200)

    def test_product_sorting_by_category(self):
        """
        Ensure products can be sorted by category.
        """
        response = self.client.get(reverse('products'), {
            'sort': 'category',
            'direction': 'desc'
        })
        self.assertEqual(response.status_code, 200)

    def test_product_category_filter(self):
        """
        Ensure product category filter returns correct result.
        """
        response = self.client.get(reverse('products'), {
            'category': self.category.name
        })
        self.assertContains(response, 'Test Product')

    def test_add_product_permission_denied_for_non_admin(self):
        """
        Ensure that non-superusers cannot access the add_product view.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('add_product'))
        self.assertRedirects(response, reverse('home'))

    def test_add_product_view_for_admin(self):
        """
        Ensure superusers can access the add_product view.
        """
        self.client.login(username='adminuser', password='adminpass')
        response = self.client.get(reverse('add_product'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/add_product.html')

    def test_edit_product_view_get_admin(self):
        """
        Superuser can access the edit form and sees product info message.
        """
        self.client.login(username='adminuser', password='adminpass')
        url = reverse('edit_product', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/edit_product.html')
        self.assertContains(response, 'You are editing')

    def test_edit_product_permission_denied(self):
        """
        Ensure non-superusers are redirected from the edit_product view.
        """
        self.client.login(username='testuser', password='testpass')
        url = reverse('edit_product', args=[self.product.id])
        response = self.client.get(url)
        self.assertRedirects(response, reverse('home'))

    def test_edit_product_view_post_valid(self):
        """
        Superusers can post valid changes to edit_product view.
        """
        self.client.login(username='adminuser', password='adminpass')
        url = reverse('edit_product', args=[self.product.id])
        response = self.client.post(url, {
            'name': 'Updated Name',
            'description': 'Updated description',
            'category': self.category.id,
            'has_variants': True,
        })
        self.assertRedirects(
            response, reverse('product_detail', args=[self.product.id])
        )
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Name')

    def test_edit_product_view_post_invalid(self):
        """
        Superusers submitting invalid form data receive an error.
        """
        self.client.login(username='adminuser', password='adminpass')
        url = reverse('edit_product', args=[self.product.id])
        response = self.client.post(url, {'name': ''})  # Name is required
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/edit_product.html')
        form = response.context['form']
        self.assertIn('name', form.errors)
        self.assertIn('This field is required.', form.errors['name'])

    def test_delete_product_permission_denied(self):
        """
        Ensure non-superusers cannot delete products.
        """
        self.client.login(username='testuser', password='testpass')
        url = reverse('delete_product', args=[self.product.id])
        response = self.client.get(url)
        self.assertRedirects(response, reverse('home'))

    def test_delete_product_view_for_admin(self):
        """
        Ensure superusers can delete products and are redirected after.
        """
        self.client.login(username='adminuser', password='adminpass')
        url = reverse('delete_product', args=[self.product.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('products'))
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

    def test_add_product_invalid_form(self):
        """
        Admin submitting invalid product form should see an error.
        """
        self.client.login(username='adminuser', password='adminpass')
        response = self.client.post(reverse('add_product'), {
            'name': '',
            'description': 'Missing name',
            'has_variants': True
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/add_product.html')
        form = response.context['form']
        self.assertIn('name', form.errors)
        self.assertIn('This field is required.', form.errors['name'])

    def test_add_product_invalid_form_and_formset(self):
        """
        Both product form and variant formset invalid
        should show error message.
        """
        self.client.login(username='adminuser', password='adminpass')
        response = self.client.post(reverse('add_product'), {
            'name': '',  # missing required field
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/add_product.html')
        messages = list(response.context['messages'])
        self.assertTrue(
            any("Failed to add product" in str(m) for m in messages)
        )
