from decimal import Decimal

from django.conf import settings
from django.shortcuts import get_object_or_404

from products.models import Product
from profiles.models import UserProfile

MEMBER_DISCOUNT_RATE = Decimal('0.10')


def bag_contents(request):
    """
    Calculate bag totals, apply member discount if eligible,
    and return all relevant context variables.
    """
    bag_items = []
    total = Decimal('0.00')
    product_count = 0
    bag = request.session.get('bag', {})
    discount = Decimal('0.00')
    is_member = False

    for item_id, item_data in bag.items():
        product = get_object_or_404(Product, pk=int(item_id))

        if isinstance(item_data, int):
            # Non-variant fallback
            price = product.price
            subtotal = item_data * price
            total += subtotal
            product_count += item_data
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
                'price': price,
                'subtotal': subtotal,
            })
            continue

        for variant_key, quantity in item_data.get(
            'items_by_variant', {}
        ).items():
            size, colour = variant_key.split('_')
            size = size.upper()
            colour = colour.capitalize()
            variant = product.variants.filter(
                size=size, colour=colour
            ).first()

            if variant:
                price = variant.price
                subtotal = Decimal(quantity) * price
                total += subtotal
                product_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'variant': variant,
                    'sku': variant.sku,
                    'price': price,
                    'subtotal': subtotal,
                    'variant_key': variant_key,
                })

    # Apply member discount
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            if profile.is_member:
                is_member = True
                discount = total * MEMBER_DISCOUNT_RATE
        except UserProfile.DoesNotExist:
            pass

    discount = round(discount, 2)
    total_after_discount = total - discount

    # Delivery logic
    if total_after_discount < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total_after_discount * (
            Decimal(settings.STANDARD_DELIVERY_PERCENTAGE) / 100
        )
        free_delivery_delta = (
            settings.FREE_DELIVERY_THRESHOLD - total_after_discount
        )
    else:
        delivery = Decimal('0.00')
        free_delivery_delta = Decimal('0.00')

    grand_total = total_after_discount + delivery

    return {
        'bag_items': bag_items,
        'total': total,
        'discount': discount,
        'total_after_discount': total_after_discount,
        'product_count': product_count,
        'delivery': round(delivery, 2),
        'free_delivery_delta': round(free_delivery_delta, 2),
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': round(grand_total, 2),
        'is_member': is_member,
    }
