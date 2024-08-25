from typing import cast
from django.http import HttpResponse
from django.shortcuts import render

from notifications.models import EmailTemplate, SentEmail


def view_empty_template(request):
    return render(
        request,
        "notifications/email-template.html",
        {
            "subject": "{{subject}}",
            "preview_text": "{{preview_text}}",
            "body": "{{body}}",
        },
    )


def view_email_template(request, object_id):
    email_template = cast(EmailTemplate, EmailTemplate.objects.get(id=object_id))
    html_body = email_template.render(show_placeholders=True).html_body
    return render(
        request,
        "notifications/admin-email-template-preview.html",
        {
            "html_body": html_body,
            "placeholders": email_template.get_placeholders_available(),
        },
    )


def view_sent_email(request, object_id):
    sent_email = cast(SentEmail, SentEmail.objects.get(id=object_id))
    return HttpResponse(sent_email.body)
