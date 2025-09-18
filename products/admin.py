from django.utils.html import format_html
from django.contrib import admin
from .models import Category, Product, ProductVariant

class CategoryAdmin(admin.ModelAdmin):
        list_display = ('friendly_name', 'name',)


class ProductVariantInline(admin.TabularInline):  # Or use StackedInline if you prefer
    model = ProductVariant
    extra = 1  # Number of blank variant forms shown by default
    show_change_link = True
    verbose_name_plural = "Variants"
    readonly_fields = ['preview']
    fields = ('sku', 'price', 'stock', 'size', 'colour', 'image', 'preview')
    
    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 60px;" />', obj.image.url)
        return "(No image)"

    preview.short_description = 'Image Preview'


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'has_variants', 'image_preview')
    ordering = ('name',)
    inlines = [ProductVariantInline]
    readonly_fields = ['image_preview']
    fields = ('name', 'category', 'has_variants', 'description', 'image', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 100px;" />', obj.image.url)
        return "(No image)"

    image_preview.short_description = 'Image Preview'


class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('sku', 'product', 'price', 'stock', 'size', 'colour', 'variant_image_preview')
    readonly_fields = ['variant_image_preview']

    def variant_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 60px;" />', obj.image.url)
        return "(No image)"

    variant_image_preview.short_description = 'Image Preview'


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
