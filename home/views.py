from django.shortcuts import render


def index(request):
    """ A view to return the index page """
    
    return render(request, 'home/index.html')

def custom_404(request, exception):
    """
    Custom 404 error handler.

    Renders a friendly 404 page when a page is not found.
    Django automatically passes the exception as a second argument.
    """
    return render(request, '404.html', status=404)
