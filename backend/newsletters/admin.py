from django.contrib import admin

from newsletters.forms import SendEmailForm

from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        submitted = False

        if request.method == "POST":
            form = SendEmailForm(request.POST)
            if form.is_valid():
                submitted = True
        else:
            form = SendEmailForm()

        extra_context.update({"form": form, "submitted": submitted})
        return super(SubscriptionAdmin, self).changelist_view(
            request, extra_context=extra_context
        )
