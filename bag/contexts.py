from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product, ProductVariant

def bag_contents(request):
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, item_data in bag.items():
        product = get_object_or_404(Product, pk=int(item_id))

        if isinstance(item_data, int):
            print("Item with no variants:", item_id)
            # fallback for non-variant products (if you have any)
            continue

        # Variant items
        for variant_key, quantity in item_data.get('items_by_variant', {}).items():
            print(f"Processing variant: {variant_key} (qty {quantity})")
            size, colour = variant_key.split('_')
            size = size.upper()
            colour = colour.capitalize()
            variant = product.variants.filter(size=size, colour=colour).first()

            if variant:
                price = variant.price
                total += quantity * price
                product_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'variant': variant,
                    'subtotal': quantity * price,
                })
                print(f"Added to bag_items: {variant} x{quantity}")
            else:
                print(f"Variant not found for key {variant_key}")

            print("FINAL product_count:", product_count)

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
