from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST

from products.models import Product

def view_bag(request):
    """A view that renders the bag contents page."""
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """Add a quantity of a specific variant (size + colour) to the shopping bag."""
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = request.POST.get('variant_size')
    colour = request.POST.get('variant_colour')

    bag = request.session.get('bag', {})
    item_id_str = str(item_id)
    variant_key = f"{size}_{colour}".lower() if size and colour else None

    if variant_key:
        if item_id_str in bag:
            bag[item_id_str].setdefault('items_by_variant', {})
            if variant_key in bag[item_id_str]['items_by_variant']:
                bag[item_id_str]['items_by_variant'][variant_key] += quantity
                messages.success(request,
                    f"Updated {product.name} ({size.upper()}, {colour.capitalize()}) quantity to {bag[item_id_str]['items_by_variant'][variant_key]}")
            else:
                bag[item_id_str]['items_by_variant'][variant_key] = quantity
                messages.success(request,
                    f"Added {product.name} ({size.upper()}, {colour.capitalize()}) to your bag")
        else:
            bag[item_id_str] = {'items_by_variant': {variant_key: quantity}}
            messages.success(request,
                f"Added {product.name} ({size.upper()}, {colour.capitalize()}) to your bag")
    else:
        # No variant fallback
        if item_id_str in bag:
            bag[item_id_str] += quantity
            messages.success(request, f"Updated {product.name} quantity to {bag[item_id_str]}")
        else:
            bag[item_id_str] = quantity
            messages.success(request, f"Added {product.name} to your bag")

    request.session['bag'] = bag
    return redirect(redirect_url)


@require_POST
def adjust_bag(request, item_id):
    """Adjust the quantity of a specific product variant in the bag."""
    product = get_object_or_404(Product, pk=item_id)
    size = request.POST.get('variant_size')
    colour = request.POST.get('variant_colour')
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')

    bag = request.session.get('bag', {})
    item_id_str = str(item_id)
    variant_key = f"{size}_{colour}".lower()

    if item_id_str in bag and 'items_by_variant' in bag[item_id_str]:
        if quantity > 0:
            bag[item_id_str]['items_by_variant'][variant_key] = quantity
            messages.success(request,
                f"Updated {product.name} ({size.upper()}, {colour.capitalize()}) quantity to {quantity}")
        else:
            # Quantity = 0: remove variant
            bag[item_id_str]['items_by_variant'].pop(variant_key, None)
            if not bag[item_id_str]['items_by_variant']:
                bag.pop(item_id_str, None)
            messages.success(request,
                f"Removed {product.name} ({size.upper()}, {colour.capitalize()}) from your bag")
    else:
        messages.error(request, "Unable to update item - not found in bag")

    request.session['bag'] = bag
    return redirect(redirect_url)


@require_POST
def remove_from_bag(request, item_id):
    """Remove a specific variant (size + colour) of a product from the shopping bag."""
    try:
        size = request.POST.get('product_size')
        colour = request.POST.get('product_colour')
        variant_key = f"{size}_{colour}".lower()
        bag = request.session.get('bag', {})
        item_id_str = str(item_id)

        product = get_object_or_404(Product, pk=item_id)

        if item_id_str in bag and 'items_by_variant' in bag[item_id_str]:
            if variant_key in bag[item_id_str]['items_by_variant']:
                del bag[item_id_str]['items_by_variant'][variant_key]

                if not bag[item_id_str]['items_by_variant']:
                    del bag[item_id_str]

                messages.success(request,
                    f"Removed {product.name} ({size.upper()}, {colour.capitalize()}) from your bag")
            else:
                messages.error(request, "Item not found in bag")
        else:
            messages.error(request, "Item not found in bag")

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f"Error removing item: {e}")
        return HttpResponse(status=500)
    
    
@require_POST
def update_bag_all(request):
    """Update multiple variant quantities from the 'Update Basket' form."""
    bag = request.session.get('bag', {})

    # Count how many items were submitted
    item_count = len([key for key in request.POST if key.startswith('item_id_')])

    for i in range(1, item_count + 1):
        item_id = request.POST.get(f'item_id_{i}')
        variant_key = request.POST.get(f'variant_key_{i}')
        quantity = int(request.POST.get(f'quantity_{i}'))

        product = get_object_or_404(Product, pk=item_id)
        item_id_str = str(item_id)

        if item_id_str in bag and 'items_by_variant' in bag[item_id_str]:
            if quantity > 0:
                bag[item_id_str]['items_by_variant'][variant_key] = quantity
                size, colour = variant_key.split('_')
                messages.success(
                    request,
                    f"Updated {product.name} ({size.upper()}, {colour.capitalize()}) quantity to {quantity}"
                )
            else:
                # Quantity = 0, remove variant
                bag[item_id_str]['items_by_variant'].pop(variant_key, None)
                if not bag[item_id_str]['items_by_variant']:
                    bag.pop(item_id_str, None)
                size, colour = variant_key.split('_')
                messages.success(
                    request,
                    f"Removed {product.name} ({size.upper()}, {colour.capitalize()}) from your bag"
                )

    request.session['bag'] = bag
    return redirect('view_bag')

