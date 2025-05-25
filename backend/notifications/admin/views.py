from typing import cast
from django.http import HttpResponse

from notifications.models import EmailTemplate, SentEmail


def view_email_template(request, object_id):
    email_template = cast(EmailTemplate, EmailTemplate.objects.get(id=object_id))
    html_body = email_template.render(
        show_placeholders=True,
        placeholders={key: values[0] for key, values in dict(request.GET).items()},
    ).html_body
    return HttpResponse(html_body)


def view_sent_email(request, object_id):
    sent_email = cast(SentEmail, SentEmail.objects.get(id=object_id))
    return HttpResponse(
        sent_email.body_file.read().decode("utf-8")
        if sent_email.body_file
        else sent_email.body
    )
