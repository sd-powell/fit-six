from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, ProductVariant, Category


class ProductVariantForm(forms.ModelForm):
    """
    Form for creating and editing ProductVariant instances.

    Allows admin users to manage size, colour, price, stock,
    and associated images for each product variant.
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
        - Ensures all image fields use custom file input widgets.
        """
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.HiddenInput):
                field.widget.attrs.update({
                    'class': 'border-black rounded-0 form-control-sm',
                })


class ProductForm(forms.ModelForm):
    """
    Form for creating and editing Product instances.

    Includes support for custom image upload handling
    and dynamically populates category choices using
    friendly category names.
    """
    image = forms.ImageField(
        label='Main Product Image',
        required=False,
        widget=CustomClearableFileInput
    )

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """
        Initialise the ProductForm.

        - Populates category dropdown with friendly names.
        - Applies consistent Bootstrap styling to all fields.
        """
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        self.fields['category'].choices = friendly_names

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'border-black rounded-0 form-control-sm',
            })
