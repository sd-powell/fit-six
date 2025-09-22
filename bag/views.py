from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import Product


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of a specific variant (size + colour) to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = request.POST.get('variant_size')
    colour = request.POST.get('variant_colour')

    bag = request.session.get('bag', {})
    item_id_str = str(item_id)  # <- convert to string

    variant_key = f"{size}_{colour}".lower() if size and colour else None

    if variant_key:
        if item_id_str in bag:
            if 'items_by_variant' in bag[item_id_str]:
                if variant_key in bag[item_id_str]['items_by_variant']:
                    bag[item_id_str]['items_by_variant'][variant_key] += quantity
                    messages.success(
                        request,
                        f"Updated {product.name} ({size.upper()}, {colour.capitalize()}) quantity to {bag[item_id_str]['items_by_variant'][variant_key]}"
                    )
                else:
                    bag[item_id_str]['items_by_variant'][variant_key] = quantity
                    messages.success(
                        request,
                        f"Added {product.name} ({size.upper()}, {colour.capitalize()}) to your bag"
                    )
            else:
                bag[item_id_str]['items_by_variant'] = {variant_key: quantity}
                messages.success(
                    request,
                    f"Added {product.name} ({size.upper()}, {colour.capitalize()}) to your bag"
                )
        else:
            bag[item_id_str] = {'items_by_variant': {variant_key: quantity}}
            messages.success(
                request,
                f"Added {product.name} ({size.upper()}, {colour.capitalize()}) to your bag"
            )
    else:
        # No variants (fallback)
        if item_id_str in bag:
            bag[item_id_str] += quantity
            messages.success(request, f"Updated {product.name} quantity to {bag[item_id_str]}")
        else:
            bag[item_id_str] = quantity
            messages.success(request, f"Added {product.name} to your bag")

    request.session['bag'] = bag
    return redirect(redirect_url)

