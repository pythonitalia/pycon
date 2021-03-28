from typing import Optional

from pythonit_toolkit.emails import get_email_backend
from pythonit_toolkit.emails.templates import EmailTemplate
from users.settings import DEFAULT_EMAIL_FROM, EMAIL_BACKEND, ENVIRONMENT


def send_email(
    *,
    template: EmailTemplate,
    to: str,
    subject: str,
    from_: Optional[str] = None,
    variables: Optional[dict[str, str]] = None
):
    from_ = from_ or DEFAULT_EMAIL_FROM
    backend = get_email_backend(EMAIL_BACKEND, environment=ENVIRONMENT)
    backend.send_email(
        template=template, from_=from_, to=to, subject=subject, variables=variables
    )
