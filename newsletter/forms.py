from django import forms
from .models import NewsletterSignup


class NewsletterSignupForm(forms.ModelForm):
    """
    Form to handle user input for newsletter signup.

    Collects and validates an email address, optionally linking it
    to a UserProfile if provided in the view.
    Prevents duplicate subscriptions and whitespace-only input.
    """
    class Meta:
        model = NewsletterSignup
        fields = ['email']

    def __init__(self, *args, **kwargs):
        """
        Customise the email input field:
        - Add placeholder, class styling
        - Prevent whitespace-only submissions using HTML5 pattern
        """
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Enter your email',
            'class': 'border-black rounded-0',
            'pattern': r'.*\S.*',
            'title': 'This field cannot be blank or contain only spaces.',
        })

    def clean_email(self):
        """
        Ensure the submitted email is not already registered.
        """
        email = self.cleaned_data.get('email').lower()
        if NewsletterSignup.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already subscribed.")
        return email
