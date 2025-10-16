"""Custom template filters for the Bag app."""
from django import template

register = template.Library()


@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    """
    Calculate the subtotal for a cart item.

    Multiplies the unit price by the quantity to return the subtotal value.
    If either value is invalid (e.g., None or non-numeric), returns 0 instead
    of raising an exception.

    Args:
        price (float | int): The price of a single item.
        quantity (int): The quantity of that item.

    Returns:
        float: The subtotal (price × quantity) or 0 on error.
    """
    try:
        return price * quantity
    except (TypeError, ValueError):
        return 0
