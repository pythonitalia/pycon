from django.http import HttpResponse
from django.shortcuts import render

from notifications.models import SentEmail


def view_base_template(request):
    return render(
        request,
        "notifications/email-template.html",
        {
            "subject": "{{subject}}",
            "preview_text": "{{preview_text}}",
            "body": "{{body}}",
        },
    )


def view_sent_email(request, object_id):
    sent_email = SentEmail.objects.get(id=object_id)
    return HttpResponse(sent_email.body)
