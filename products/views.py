from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Min
from .models import Product, Category
from django.db.models.functions import Lower

"""
Product app views.
Handles listing, filtering, and detail display of products.
"""


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    # Prefetch related variants to reduce DB queries on product list view
    products = Product.objects.prefetch_related('variants').all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey

            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            elif sortkey == 'category':
                sortkey = 'category__name'

            elif sortkey == 'price':
                sortkey = 'min_price'
                products = products.annotate(min_price=Min('variants__price'))

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'

            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    variants = product.variants.all()

    # Get distinct colours and sizes
    colours = variants.values_list('colour', flat=True).distinct()
    sizes = variants.values_list('size', flat=True).distinct()

    return render(request, 'products/product_detail.html', {
        'product': product,
        'variants': variants,
        'colours': colours,
        'sizes': sizes,
    })
