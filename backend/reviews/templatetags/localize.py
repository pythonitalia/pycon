from django import template

register = template.Library()


@register.filter
def localize(value, language: str):
    return value.localize(language)
