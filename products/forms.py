from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, ProductVariant, Category


class ProductVariantForm(forms.ModelForm):
    """
    Form for creating and editing ProductVariant instances.

    Allows admin users to manage size, colour, price, and stock
    details for individual product variants.
    """
    image = forms.ImageField(
        label='Front Image',
        required=False,
        widget=CustomClearableFileInput
    )
    image_back = forms.ImageField(
        label='Back Image',
        required=False,
        widget=CustomClearableFileInput
    )

    class Meta:
        model = ProductVariant
        fields = ['size', 'colour', 'price', 'stock', 'image', 'image_back']

    def __init__(self, *args, **kwargs):
        """
        Initialise the ProductVariantForm.

        - Applies consistent Bootstrap styling to all visible fields.
        - Excludes hidden fields like 'id' from styling.
        """
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ != 'HiddenInput':
                field.widget.attrs['class'] = 'border-black rounded-0'


class ProductForm(forms.ModelForm):
    """
    Form for creating and editing Product instances.

    Includes support for custom image upload handling
    and dynamically populates category choices using
    friendly category names.
    """
    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(
        label='Image',
        required=False,
        widget=CustomClearableFileInput
    )

    def __init__(self, *args, **kwargs):
        """
        Initialise the ProductForm.

        - Populates the category dropdown with friendly names.
        - Adds consistent Bootstrap styling to all form fields.
        """
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
