from decimal import Decimal
from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404
)
from django.contrib import messages
from django.views.decorators.http import require_POST

from products.models import Product
from profiles.models import UserProfile

# Member discount rate (10%)
MEMBER_DISCOUNT_RATE = Decimal('0.10')


def view_bag(request):
    """Render the bag contents page, with optional member discount."""
    bag = request.session.get('bag', {})
    bag_items = []
    total = 0
    product_count = 0

    # Calculate totals
    for item_id, item_data in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        if isinstance(item_data, int):
            # Product without variants
            price = product.price
            subtotal = Decimal(item_data) * price
            total += subtotal
            product_count += item_data
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
                'price': price,
                'subtotal': subtotal,
            })
        else:
            # Product with variants
            for variant_key, quantity in item_data.get(
                'items_by_variant', {}
            ).items():
                variant = product.variants.first()
                price = variant.price if variant else product.price
                subtotal = Decimal(quantity) * price
                total += subtotal
                product_count += quantity

                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'variant_key': variant_key,
                    'price': price,
                    'subtotal': subtotal,
                })

    # --- Member discount logic ---
    discount = 0
    is_member = False

    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            if profile.is_member:
                discount = total * MEMBER_DISCOUNT_RATE
                is_member = True
        except UserProfile.DoesNotExist:
            pass

    grand_total = total - discount

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'discount': round(discount, 2),
        'grand_total': grand_total,
        'is_member': is_member,
    }
    return render(request, 'bag/bag.html', context)


def add_to_bag(request, item_id):
    """Add a quantity of a specific variant (size + colour) to the bag."""
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
                new_qty = bag[item_id_str]['items_by_variant'][variant_key]
                messages.success(
                    request,
                    f"Updated {product.name} ({size.upper()}, "
                    f"{colour.capitalize()}) quantity to {new_qty}"
                )
            else:
                bag[item_id_str]['items_by_variant'][variant_key] = quantity
                messages.success(
                    request,
                    f"Added {product.name} ({size.upper()}, "
                    f"{colour.capitalize()}) to your bag"
                )
        else:
            bag[item_id_str] = {'items_by_variant': {variant_key: quantity}}
            messages.success(
                request,
                f"Added {product.name} ({size.upper()}, "
                f"{colour.capitalize()}) to your bag"
            )
    else:
        # No variant fallback
        if item_id_str in bag:
            bag[item_id_str] += quantity
            messages.success(
                request,
                f"Updated {product.name} quantity to {bag[item_id_str]}"
            )
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
            messages.success(
                request,
                f"Updated {product.name} ({size.upper()}, "
                f"{colour.capitalize()}) quantity to {quantity}"
            )
        else:
            # Quantity = 0: remove variant
            bag[item_id_str]['items_by_variant'].pop(variant_key, None)
            if not bag[item_id_str]['items_by_variant']:
                bag.pop(item_id_str, None)
            messages.success(
                request,
                f"Removed {product.name} ({size.upper()}, "
                f"{colour.capitalize()}) from your bag"
            )
    else:
        messages.error(request, "Unable to update item - not found in bag")

    request.session['bag'] = bag
    return redirect(redirect_url)


@require_POST
def remove_from_bag(request, item_id):
    """Remove a specific variant (size + colour) of a product from the bag."""
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
                messages.success(
                    request,
                    f"Removed {product.name} ({size.upper()}, "
                    f"{colour.capitalize()}) from your bag"
                )
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
    item_count = len([
        key for key in request.POST if key.startswith('item_id_')
    ])

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
                    f"Updated {product.name} ({size.upper()}, "
                    f"{colour.capitalize()}) quantity to {quantity}"
                )
            else:
                # Quantity = 0: remove variant
                bag[item_id_str]['items_by_variant'].pop(variant_key, None)
                if not bag[item_id_str]['items_by_variant']:
                    bag.pop(item_id_str, None)
                size, colour = variant_key.split('_')
                messages.success(
                    request,
                    f"Removed {product.name} ({size.upper()}, "
                    f"{colour.capitalize()}) from your bag"
                )

    request.session['bag'] = bag
    return redirect('view_bag')
