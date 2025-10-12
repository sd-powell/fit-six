from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):
    """
    Category model for grouping products.
    """
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=254)
    slug = models.SlugField(max_length=254, unique=True, blank=True, null=False, editable=False)
    description = models.TextField()
    has_variants = models.BooleanField(default=False)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
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
        return (
            f"{self.product.name} - "
            f"{self.size or 'One Size'} - "
            f"{self.colour or 'Default'}"
        )
