from ordered_model.admin import (
    OrderedInlineModelAdminMixin,
    OrderedModelAdmin,
    OrderedTabularInline,
)
from django.contrib import admin

from visa.models import (
    InvitationLetterAttachedDocument,
    InvitationLetterOrganizerConfig,
    InvitationLetterRequest,
)


def process_invitation_letter(modeladmin, request, queryset):
    for invitation_letter_request in queryset:
        invitation_letter_request.process()


@admin.register(InvitationLetterRequest)
class InvitationLetterRequestAdmin(admin.ModelAdmin):
    list_display = (
        "conference",
        "requester",
        "on_behalf_of",
        "full_name",
        "nationality",
        "status",
    )
    list_filter = (
        "status",
        "conference",
    )
    autocomplete_fields = [
        "requester",
    ]
    search_fields = [
        "full_name",
        "requester__email",
    ]
    actions = [process_invitation_letter]


class InvitationLetterAttachedDocumentInline(OrderedTabularInline):
    fields = ("document", "order", "move_up_down_links")
    readonly_fields = (
        "order",
        "move_up_down_links",
    )
    model = InvitationLetterAttachedDocument
    extra = 0
    verbose_name = "Attached document"
    verbose_name_plural = "Attached documents"
    ordering = ("order",)


@admin.register(InvitationLetterOrganizerConfig)
class InvitationLetterOrganizerConfigAdmin(
    OrderedInlineModelAdminMixin, OrderedModelAdmin
):
    list_display = ("organizer",)
    search_fields = [
        "organizer__name",
    ]
    inlines = [InvitationLetterAttachedDocumentInline]
