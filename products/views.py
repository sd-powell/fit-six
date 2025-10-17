from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.db.models import Q, Min, Max
from django.db.models.functions import Lower
import json
from uuid import uuid4

from .models import Product, ProductVariant, Category
from .forms import ProductForm, ProductVariantForm

ProductVariantFormSet = inlineformset_factory(
    Product,
    ProductVariant,
    form=ProductVariantForm,
    fields=('id', 'size', 'colour', 'price', 'stock', 'image', 'image_back'),
    extra=0,
    can_delete=True
)


def all_products(request):
    """
    Display all products, with optional sorting, category filtering,
    and search functionality.

    Supports:
    - Sorting by name, category, or lowest variant price.
    - Filtering by category name(s).
    - Searching by name or description.
    - Annotates products with min/max variant prices for display logic.
    """
    # Annotate each product with its min and max variant prices
    products = (
        Product.objects.prefetch_related('variants')
        .annotate(
            min_price=Min('variants__price'),
            max_price=Max('variants__price')
        )
    )

    query = None
    categories = None
    sort = None
    direction = None
    selected_category = None

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
            if categories.count() == 1:
                selected_category = categories.first().friendly_name

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request,
                    "You didn't enter any search criteria!"
                    )
                return redirect(reverse('products'))

            queries = (
                    Q(name__icontains=query) |
                    Q(description__icontains=query)
            )
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    # Manually ensure min_price and max_price for non-variant products
    for product in products:
        if not product.has_variants:
            variant = product.variants.first()
            if variant:
                setattr(product, 'min_price', variant.price)
                setattr(product, 'max_price', variant.price)

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'selected_category': selected_category,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


# products/views.py
def product_detail(request, slug):
    """
    Display the detail page for a single product.

    Retrieves all related product variants and prepares data for:
    - Available sizes and colours (excluding empty/null values)
    - Mapping each colour to its associated front and back images
    - Mapping each size/colour combination to its price for dynamic updates
    - Rendering colour and size selectors only when applicable

    Args:
        request (HttpRequest): The incoming request object.
        slug (str): The unique slug used to identify the product.

    Returns:
        HttpResponse: Rendered product detail page with product
        and variant context.
    """
    product = get_object_or_404(Product, slug=slug)
    variants = product.variants.all()

    # Distinct dropdown data
    colours = (
        variants.exclude(colour__isnull=True)
        .exclude(colour__exact='')
        .values_list('colour', flat=True)
        .distinct()
    )
    sizes = variants.values_list('size', flat=True).distinct()

    # Build a dictionary of variant data per colour (for image display)
    colour_image_map = {}
    for variant in variants:
        if variant.colour not in colour_image_map:
            colour_image_map[variant.colour] = {
                'image_url': variant.image.url if variant.image else '',
                'image_back_url': (
                    variant.image_back.url
                    if variant.image_back
                    else ''
                ),
            }

    # Build a variant price map for dynamic JS updates
    variant_price_map = {}
    for variant in variants:
        size = variant.size or ''
        colour = variant.colour or ''
        key = f"{size}_{colour}"
        variant_price_map[key] = float(variant.price)

    context = {
        'product': product,
        'variants': variants,
        'colours': colours,
        'sizes': sizes,
        'colour_image_map': colour_image_map,
        # Safe JSON to render in template
        'variant_price_map': mark_safe(json.dumps(variant_price_map)),
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """
    Allow superusers to add a new product and its variants.

    - Validates the main product form and associated inline formset.
    - On success, redirects to the product detail page.
    - Displays error messages if form or formset is invalid.
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    # Local inlineformset with extra=1
    ProductVariantFormSet = inlineformset_factory(
        Product,
        ProductVariant,
        form=ProductVariantForm,
        fields=(
            'id',
            'size',
            'colour',
            'price',
            'stock',
            'image',
            'image_back'
        ),
        extra=1,  # Show one empty form by default on "add"
        can_delete=True
    )

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        formset = ProductVariantFormSet(
            request.POST or None, prefix='variants'
        )
        if form.is_valid() and formset.is_valid():
            product = form.save()
            formset.instance = product
            variants = formset.save(commit=False)

            for variant in variants:
                # Check for duplicate size+colour for this product
                exists = ProductVariant.objects.filter(
                    product=product,
                    size=variant.size,
                    colour=variant.colour
                ).exists()

                if exists:
                    messages.warning(
                        request,
                        f"Duplicate variant skipped: "
                        f"{variant.size or 'N/A'} / {variant.colour or 'N/A'}"
                    )
                    continue

                # Assign SKU if missing
                if not variant.sku:
                    variant.sku = str(uuid4())[:8].upper()

                variant.save()

            formset.save_m2m()
            messages.success(
                request, 'Successfully added product and variants!'
            )
            return redirect('product_detail', slug=product.slug)
        else:
            messages.error(
                request,
                'Failed to add product. Please check the form and variants.'
            )
    else:
        form = ProductForm()
        formset = ProductVariantFormSet(prefix='variants')

    template = 'products/add_product.html'
    context = {
        'form': form,
        'formset': formset,
    }

    return render(request, template, context)


@login_required
def edit_product(request, slug):
    """
    Allow superusers to edit an existing product's details, including variants.
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, slug=slug)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        variant_formset = ProductVariantFormSet(
            request.POST,
            instance=product,
            queryset=ProductVariant.objects.filter(product=product),
        )

        if form.is_valid() and variant_formset.is_valid():
            form.save()
            variant_formset.save()
            messages.success(
                request, 'Successfully updated product and variants!'
            )
            return redirect('product_detail', slug=product.slug)
        else:
            print("Product form errors:", form.errors)
            print("Variant formset errors:")
            for variant_form in variant_formset:
                print(variant_form.errors)
            messages.error(
                request,
                'Failed to update product or variants.'
                'Please ensure the form is valid.'
            )
    else:
        form = ProductForm(instance=product)
        variant_formset = ProductVariantFormSet(
            instance=product,
            queryset=ProductVariant.objects.filter(product=product),
        )
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'variant_formset': variant_formset,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, slug):
    """
    Allow superusers to delete a product from the store.

    Args:
        slug (str): The slug of the product to delete.
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, slug=slug)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))
