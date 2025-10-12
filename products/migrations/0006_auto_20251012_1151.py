from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('products', '0005_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(
                max_length=254,
                blank=True,
                null=False,
                unique=True,
                editable=False,
            ),
        ),
    ]
