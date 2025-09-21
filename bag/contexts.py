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
        product = get_object_or_404(Product, pk=item_id)

        if isinstance(item_data, int):
            # No variants, fallback
            variant = product.variants.first()
            price = variant.price if variant else 0
            total += item_data * price
            product_count += item_data
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
                'variant': variant,
            })

        else:
            for variant_key, quantity in item_data['items_by_variant'].items():
                # Split variant_key like "s_black" into "s" and "black"
                try:
                    size, colour = variant_key.split('_')
                except ValueError:
                    size, colour = variant_key, None

                # Find matching variant
                variant = product.variants.filter(size=size, colour=colour).first()

                if not variant:
                    continue  # Skip if no matching variant found

                total += quantity * variant.price
                product_count += quantity

                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'variant': variant,
                    'size': size,
                    'colour': colour,
                })

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