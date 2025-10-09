from django import template

register = template.Library()


@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    try:
        return price * quantity
    except (TypeError, ValueError):
        return 0
