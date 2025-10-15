from django.shortcuts import render


def index(request):
    """ A view to return the index page """
    
    return render(request, 'home/index.html')

def privacy(request):
    """
    View that returns the privacy policy page
    """
    return render(request, "home/privacy.html")


def terms(request):
    """
    View that returns the terms and conditions page
    """
    return render(request, "home/terms.html")


def shipping(request):
    """
    View that returns the shipping policy page
    """
    return render(request, "home/shipping.html")

def custom_404(request, exception):
    """
    Custom 404 error handler.

    Renders a friendly 404 page when a page is not found.
    Django automatically passes the exception as a second argument.
    """
    return render(request, '404.html', status=404)
