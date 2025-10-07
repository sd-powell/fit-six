from django.utils.html import format_html
from django.contrib import admin
from .models import Category, Product, ProductVariant


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('friendly_name', 'name',)


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    show_change_link = True
    verbose_name_plural = "Variants"
    readonly_fields = ['preview', 'preview_back']
    fields = (
        'sku',
        'price',
        'stock',
        'size',
        'colour',
        'image',
        'preview',
        'image_back',
        'preview_back'
        )

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height: 60px;" />',
                obj.image.url
                )
        return "(No image)"

    def preview_back(self, obj):
        if obj.image_back:
            return format_html(
                '<img src="{}" style="height: 60px;" />',
                obj.image_back.url
                )
        return "(No back image)"

    preview.short_description = 'Front Preview'
    preview_back.short_description = 'Back Preview'


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'has_variants', 'image_preview')
    ordering = ('name',)
    inlines = [ProductVariantInline]
    readonly_fields = ['image_preview']
    fields = (
        'name',
        'category',
        'has_variants',
        'description',
        'image',
        'image_preview'
        )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height: 100px;" />',
                obj.image.url
                )
        return "(No image)"

    image_preview.short_description = 'Image Preview'


class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'product',
        'price',
        'stock',
        'size',
        'colour',
        'variant_image_preview',
        'variant_back_image_preview'
        )
    readonly_fields = ['variant_image_preview', 'variant_back_image_preview']

    def variant_image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height: 60px;" />',
                obj.image.url
                )
        return "(No image)"

    def variant_back_image_preview(self, obj):
        if obj.image_back:
            return format_html(
                '<img src="{}" style="height: 60px;" />',
                obj.image_back.url
                )
        return "(No back image)"

    variant_image_preview.short_description = 'Front Image'
    variant_back_image_preview.short_description = 'Back Image'


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
