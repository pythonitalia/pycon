from typing import Optional

from api.context import Info
from django.conf import settings
from django.utils import translation


def make_localized_resolver(field_name: str):
    def resolver(root, info: Info, language: Optional[str] = None) -> str:
        language = language or translation.get_language() or settings.LANGUAGE_CODE

        return getattr(root, field_name).localize(language)

    return resolver
