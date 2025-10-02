from django.shortcuts import redirect
from django.contrib import messages
from .forms import NewsletterSignupForm


def newsletter_signup(request):
    """
    Handle newsletter signup form submissions.

    Accepts POST requests containing an email address.
    If the email is valid and not already subscribed,
    it creates a new NewsletterSignup entry in the database.
    If the email already exists, a warning message is shown.
    The user is redirected back to the referring page in both cases,
    with feedback via Django messages.
    """
    if request.method == 'POST':
        form = NewsletterSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Thanks for signing up to our newsletter!"
            )
        else:
            # Check for specific duplicate email error
            if (
                'email' in form.errors
                and any(
                    'already subscribed' in err.lower()
                    for err in form.errors['email']
                )
            ):
                messages.warning(
                    request,
                    "This email is already subscribed to our newsletter."
                )
            else:
                messages.error(
                    request,
                    "Please enter a valid email address."
                )
    return redirect(request.META.get('HTTP_REFERER', '/'))
