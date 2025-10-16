from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _


class CustomClearableFileInput(ClearableFileInput):
    """
    A custom widget extending Django's ClearableFileInput for better
    control over image upload fields in the admin and product forms.

    Customizations:
        - Updates label text for clearer user experience.
        - Uses a custom template to control layout and styling.
        - Allows users to remove or replace an existing image.

    Template:
        products/custom_widget_templates/custom_clearable_file_input.html
    """
    clear_checkbox_label = _('Remove')
    initial_text = _('Current Image')
    input_text = _('')
    template_name = (
        'products/custom_widget_templates/custom_clearable_file_input.html'
    )
