from typing import Optional

from django.conf import settings
from django.utils import translation


def make_localized_resolver(field_name: str):
    def resolver(root, info, language: Optional[str] = None) -> str:
        language = language or translation.get_language() or settings.LANGUAGE_CODE

        return getattr(root, field_name).localize(language)

    return resolver


def make_dict_localized_resolver(field_name: str):
    def resolver(root, info, language: Optional[str] = None) -> str:
        language = language or translation.get_language() or settings.LANGUAGE_CODE
        field = getattr(root, field_name)
        return field.get(language, field["en"])

    return resolver
