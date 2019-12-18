from base64 import urlsafe_b64encode

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _


def send_request_password_reset_mail(user, token):
    b64_uid = urlsafe_b64encode(bytes(str(user.id), "utf-8")).decode("utf-8")
    link = f"{settings.FRONTEND_URL}/en/reset-password/{b64_uid}/{token}"

    return send_mail(
        _("Reset password"),
        [user.email],
        "simple_email",
        {
            "heading": _("Reset your password"),
            "body": _(
                "It seems like you requested a new password!\n"
                "Use the button below to change it"
            ),
            "ctaLabel": _("Change your password"),
            "ctaLink": link,
        },
    )


def send_mail(subject, recipients, template, context={}):
    context.update({"FRONTEND_URL": settings.FRONTEND_URL})

    html_body = render_to_string(f"notifications/{template}.html", context)
    text_body = render_to_string(f"notifications/{template}.txt", context)

    message = EmailMultiAlternatives(
        subject, text_body, settings.DEFAULT_FROM_EMAIL, recipients
    )

    message.attach_alternative(html_body, "text/html")
    return message.send(False)
