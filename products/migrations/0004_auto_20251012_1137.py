from django.db import migrations
from django.utils.text import slugify
from django.db import models


def generate_unique_slugs(apps, schema_editor):
    Product = apps.get_model('products', 'Product')
    for product in Product.objects.all():
        base_slug = slugify(product.name)
        slug = base_slug
        counter = 1
        while Product.objects.filter(slug=slug).exclude(pk=product.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        product.slug = slug
        product.save()

class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_productvariant_image_back'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=254, blank=True, null=True, unique=True),
        ),
        migrations.RunPython(generate_unique_slugs),
    ]
