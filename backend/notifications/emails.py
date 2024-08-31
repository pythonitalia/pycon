from typing import List, Optional

from django.conf import settings
from notifications.templates import EmailTemplate


from dataclasses import dataclass
import importlib

from .backends.base import EmailBackend

EMAIL_BACKEND_CACHE: dict[str, EmailBackend] = {}


def get_email_backend(backend_path: str, **options: dict[str, str]) -> EmailBackend:
    global EMAIL_BACKEND_CACHE

    instance = EMAIL_BACKEND_CACHE.get(backend_path, None)

    if not instance:
        module_path, class_name = backend_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        class_impl = getattr(module, class_name)
        instance = class_impl(**options)
        EMAIL_BACKEND_CACHE[backend_path] = instance

    return instance


@dataclass
class SafeString(str):
    original_str: str

    def __str__(self) -> str:
        return self.original_str


def mark_safe(string: str) -> SafeString:
    if string is None:
        raise ValueError("string cannot be None")

    return SafeString(string)


def send_email(
    *,
    template: EmailTemplate,
    to: str,
    subject: str,
    from_: Optional[str] = None,
    variables: Optional[dict[str, str]] = None,
    reply_to: List[str] = None,
):
    from_ = from_ or settings.DEFAULT_FROM_EMAIL
    backend = get_email_backend(
        settings.PYTHONIT_EMAIL_BACKEND, environment=settings.ENVIRONMENT
    )
    backend.send_email(
        template=template,
        from_=from_,
        to=to,
        subject=subject,
        variables=variables,
        reply_to=reply_to,
    )
