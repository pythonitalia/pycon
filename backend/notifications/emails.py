from typing import Optional

from django.conf import settings
from pythonit_toolkit.emails import get_email_backend
from pythonit_toolkit.emails.templates import EmailTemplate


def send_email(
    *,
    template: EmailTemplate,
    to: str,
    subject: str,
    from_: Optional[str] = None,
    variables: Optional[dict[str, str]] = None
):
    from_ = from_ or settings.DEFAULT_EMAIL_FROM
    backend = get_email_backend(
        settings.PYTHONIT_EMAIL_BACKEND, environment=settings.ENVIRONMENT
    )
    backend.send_email(
        template=template, from_=from_, to=to, subject=subject, variables=variables
    )
