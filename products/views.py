from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Min
from .models import Product, ProductVariant, Category
from django.db.models.functions import Lower

from .forms import ProductForm, ProductVariantForm

ProductVariantFormSet = inlineformset_factory(
    Product, ProductVariant, form=ProductVariantForm,
    fields=('size', 'colour', 'price', 'stock'), extra=1, can_delete=True
)

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
            
            # If only one category selected, pass its friendly name
            selected_category = categories.first().friendly_name if categories.count() == 1 else None
        else:
            selected_category = None

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
        'selected_category': selected_category,
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


@login_required
def add_product(request):
    """ Add a product and its variants to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        formset = ProductVariantFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            product = form.save()
            formset.instance = product
            formset.save()
            messages.success(request, 'Successfully added product and variants!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please check the form and variants.')
    else:
        form = ProductForm()
        formset = ProductVariantFormSet()

    template = 'products/add_product.html'
    context = {
        'form': form,
        'formset': formset,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))
