from django.contrib import admin
from .models import Category, Product, ProductVariant

class CategoryAdmin(admin.ModelAdmin):
        list_display = (
        'friendly_name',
        'name',
    )

class ProductAdmin(admin.ModelAdmin):
        list_display = (
        'name',
        'category',
        'has_variants',
        'image',
    )

        ordering = ('name',)

class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'product',
        'price',
        'stock',
        'size',
        'colour',
    )
    ordering = ('product', 'sku',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
