import importlib
from typing import Optional

from pythonit_toolkit.emails.backends.base import EmailBackend
from pythonit_toolkit.emails.templates import EmailTemplate

from users.settings import DEFAULT_EMAIL_FROM, EMAIL_BACKEND, ENVIRONMENT

EMAIL_BACKEND_INSTANCE: Optional[EmailBackend] = None


def get_email_backend() -> EmailBackend:
    global EMAIL_BACKEND_INSTANCE

    if not EMAIL_BACKEND_INSTANCE:
        module_path, class_name = EMAIL_BACKEND.rsplit(".", 1)
        module = importlib.import_module(module_path)
        class_impl = getattr(module, class_name)
        EMAIL_BACKEND_INSTANCE = class_impl(environment=ENVIRONMENT)

    return EMAIL_BACKEND_INSTANCE


def send_email(
    *,
    template: EmailTemplate,
    to: str,
    subject: str,
    from_: Optional[str] = None,
    variables: Optional[dict[str, str]] = None
):
    from_ = from_ or DEFAULT_EMAIL_FROM
    backend = get_email_backend()
    backend.send_email(
        template=template, from_=from_, to=to, subject=subject, variables=variables
    )
