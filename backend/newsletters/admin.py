from django.contrib import admin
from newsletters.forms import SendEmailForm
from notifications.emails import send_mail

from .models import Email, Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        submitted = False

        if request.method == "POST":
            form = SendEmailForm(request.POST)
            if form.is_valid():
                submitted = self.send_emails(**form.cleaned_data)
        else:
            form = SendEmailForm()

        extra_context.update({"form": form, "submitted": submitted})
        return super(SubscriptionAdmin, self).changelist_view(
            request, extra_context=extra_context
        )

    def send_emails(self, **kwargs):
        subject = kwargs.pop("subject")
        recipients = kwargs.pop("recipients")

        return (
            send_mail(
                subject,
                recipients,
                "newsletter",
                context=kwargs,
                path="emails/newsletter/",
            )
            == 1
        )


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ("subject", "recipients_types", "send_date")
    readonly_fields = ("recipients",)
