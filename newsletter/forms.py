from django import forms
from .models import NewsletterSignup


class NewsletterSignupForm(forms.ModelForm):
    """
    Form to handle user input for newsletter signup.

    Collects and validates an email address, optionally linking it
    to a UserProfile if provided in the view.
    """
    class Meta:
        model = NewsletterSignup
        fields = ['email']

    def clean_email(self):
        """
        Ensure the submitted email is not already registered.
        """
        email = self.cleaned_data.get('email').lower()
        if NewsletterSignup.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already subscribed.")
        return email
