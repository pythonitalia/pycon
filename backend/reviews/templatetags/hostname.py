from urllib.parse import urlparse

from django import template

register = template.Library()


@register.filter
def hostname(url: str):
    parsed_url = urlparse(url)
    return parsed_url.netloc
