from django import template

register = template.Library()


@register.filter
def empty_string_if_none(value):
    return "" if value is None else value
