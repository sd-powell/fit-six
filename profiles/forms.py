from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    # Add first_name and last_name from the related User model
    first_name = forms.CharField(
        max_length=30,
        required=False,
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'First Name',
            'class': 'border-black rounded-0 profile-form-input'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Last Name',
            'class': 'border-black rounded-0 profile-form-input'
        })
    )
    
    class Meta:
        model = UserProfile
        exclude = ('user', 'is_member',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field.
        """
        user = kwargs.pop('user', None)  # Allow passing user to prefill
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
            'is_member': 'Fit Six Member?',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True

        for field in self.fields:
            if field in ['first_name', 'last_name', 'default_country']:
                continue
            placeholder = placeholders.get(field, '')
            if self.fields[field].required:
                placeholder = f'{placeholder} *'
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = (
                'border-black rounded-0 profile-form-input'
            )
            self.fields[field].label = False

        # Prefill first/last name from User if provided
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name

        # Crispy Forms layout for custom field order
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('first_name'),
            Field('last_name'),
            Field('default_street_address1'),
            Field('default_street_address2'),
            Field('default_town_or_city'),
            Field('default_county'),
            Field('default_postcode'),
            Field('default_country'),
            Field('default_phone_number'),
        )
