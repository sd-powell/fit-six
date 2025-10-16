"""Custom template filters for string manipulation in Django templates."""
from django import template

register = template.Library()


@register.filter
def split(value, delimiter="_"):
    """
    Split a string into a list using the given delimiter.

    This template filter allows you to split a string
    in a Django template by a specified delimiter.
    If no delimiter is provided, the underscore (_) is used by default.

    Args:
        value (str): The string to be split.
        delimiter (str): The delimiter to split by (default is "_").

    Returns:
        list: A list of substrings, or an empty list if the input
        is None or empty.
    """
    """Split a string into a list using the given delimiter."""
    if value:
        return value.split(delimiter)
    return []
