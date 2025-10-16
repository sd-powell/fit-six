from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):
    """
    Represents a product category used to group related products.

    Attributes:
        name (str): The internal category name used for filtering and queries.
        friendly_name (str): A user-facing version of the
        category name for display.
    """
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        """Return the category's internal name."""
        return self.name

    def get_friendly_name(self):
        """Return the user-friendly category name, if available."""
        return self.friendly_name


class Product(models.Model):
    """
    Represents an individual product that can belong to a category
    and may have variants.

    Attributes:
        category (Category): Optional reference to a product category.
        name (str): The product name.
        slug (str): A unique URL slug automatically generated
        from the product name.
        description (str): Product details and features.
        has_variants (bool): Indicates whether the product has multiple
        size/colour variants.
        image (ImageField): The main product image.
        image_url (str): Optional URL reference to an externally hosted image.
        created_at (datetime): Timestamp when the product was created.
        updated_at (datetime): Timestamp when the product was last updated.
    """
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=254)
    slug = models.SlugField(
        max_length=254,
        unique=True,
        blank=True,
        null=False,
        editable=False
    )
    description = models.TextField()
    has_variants = models.BooleanField(default=False)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Override the default save method to automatically generate
        a unique slug from the product name if one doesn't exist.
        """
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(
                slug=slug
            ).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Return the absolute URL for the product detail page.

        Used by templates and Django's reverse URL lookup system.
        """
        return reverse('product_detail', kwargs={'slug': self.slug})

    def __str__(self):
        """Return the product's name."""
        return self.name


class ProductVariant(models.Model):
    """
    Represents a specific variation of a product,
    such as a size and colour combination.

    Attributes:
        product (Product): The parent product this variant belongs to.
        sku (str): Unique stock keeping unit identifier.
        price (Decimal): The price of this variant.
        image (ImageField): Front-facing variant image.
        image_back (ImageField): Optional back image for apparel.
        stock (int): Available quantity for this variant.
        size (str): The variant’s size (e.g., S, M, L) if applicable.
        colour (str): The variant’s colour (e.g., Black, Blue) if applicable.
        created_at (datetime): Timestamp when created.
        updated_at (datetime): Timestamp when last updated.
    """
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='variants'
    )
    sku = models.CharField(max_length=254, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    image_back = models.ImageField(null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    size = models.CharField(max_length=5, null=True, blank=True)
    colour = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return a readable string representation combining
        the product name, size, and colour.
        """
        return (
            f"{self.product.name} - "
            f"{self.size or 'One Size'} - "
            f"{self.colour or 'Default'}"
        )
