from django import template

register = template.Library()


@register.filter
def split(value, delimiter="_"):
    """Split a string into a list using the given delimiter."""
    if value:
        return value.split(delimiter)
    return []
