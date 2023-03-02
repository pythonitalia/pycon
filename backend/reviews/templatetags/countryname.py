from django import template

from countries import countries

register = template.Library()


@register.filter
def countryname(country: str):
    country_data = countries.get(alpha_2=country)
    return country_data.name if country_data else ""
