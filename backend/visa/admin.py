import json
from django.utils.safestring import mark_safe

from django.urls import path
from ordered_model.admin import (
    OrderedInlineModelAdminMixin,
    OrderedModelAdmin,
    OrderedTabularInline,
)
from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import reverse
from django.http import HttpResponseRedirect

from visa.models import (
    InvitationLetterAsset,
    InvitationLetterDocument,
    InvitationLetterOrganizerConfig,
    InvitationLetterRequest,
)


@admin.register(InvitationLetterRequest)
class InvitationLetterRequestAdmin(admin.ModelAdmin):
    fields = (
        "conference",
        "requester",
        "on_behalf_of",
        "email_address",
        "full_name",
        "nationality",
        "status",
        "address",
        "date_of_birth",
        "passport_number",
        "embassy_name",
        "grant_approved_type",
        "has_travel_via_grant",
        "has_accommodation_via_grant",
        "role",
        "process_now",
        "invitation_letter",
        "send_via_email",
    )

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
    readonly_fields = (
        "process_now",
        "invitation_letter",
        "grant_approved_type",
        "role",
        "has_travel_via_grant",
        "has_accommodation_via_grant",
        "send_via_email",
    )

    def save_form(self, request, form, change):
        obj = super().save_form(request, form, change)

        if "_process_now" in form.data:
            obj.schedule()

        return obj

    def process_now(self, obj):
        return mark_safe(
            '<input type="submit" name="_process_now" value="Process now" />'
        )

    def send_via_email(self, obj):
        if not obj.invitation_letter:
            return "Generate the invitation letter first"

        return mark_safe(
            '<input type="submit" name="_send_via_email" value="Send via email" />'
        )

    def response_post_save_change(self, request, obj):
        if "_process_now" in request.POST:
            return HttpResponseRedirect(
                reverse("admin:visa_invitationletterrequest_change", args=[obj.id])
            )

        return self._response_post_save(request, obj)


class InvitationLetterAssetInline(admin.TabularInline):
    fields = (
        "identifier",
        "image",
    )
    model = InvitationLetterAsset
    extra = 0
    verbose_name = "Asset"
    verbose_name_plural = "Assets"


class InvitationLetterDocumentInline(OrderedTabularInline):
    fields = (
        "name",
        "document",
        "edit_dynamic_document",
        "order",
        "move_up_down_links",
    )
    readonly_fields = (
        "order",
        "move_up_down_links",
        "edit_dynamic_document",
    )
    model = InvitationLetterDocument
    extra = 0
    verbose_name = "Attached document"
    verbose_name_plural = "Attached documents"
    ordering = ("order",)

    def edit_dynamic_document(self, obj):
        if obj.document or not obj.id:
            return ""

        url = reverse(
            "admin:edit_dynamic_document",
            kwargs={
                "config_id": obj.invitation_letter_organizer_config_id,
                "document_id": obj.id,
            },
        )
        return mark_safe(f'<a href="{url}">Edit</a>')

    def edit_dynamic_document_view(self, request, config_id, document_id):
        document = InvitationLetterDocument.objects.get(id=document_id)
        config = document.invitation_letter_organizer_config
        assert config.id == config_id

        context = dict(
            self.admin_site.each_context(request),
            arguments={
                "document_id": document_id,
                "breadcrumbs": json.dumps(
                    self._create_builder_breadcrumbs(config, document)
                ),
            },
            title="Invitation Letter Document Builder",
        )
        return TemplateResponse(
            request, "astro/invitation-letter-document-builder.html", context
        )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:config_id>/edit_dynamic_document/<int:document_id>/",
                self.admin_site.admin_view(self.edit_dynamic_document_view),
                name="edit_dynamic_document",
            ),
        ]
        return custom_urls + urls

    def _create_builder_breadcrumbs(self, config, document):
        return [
            {
                "title": "Visa",
                "url": reverse("admin:app_list", kwargs={"app_label": "visa"}),
            },
            {
                "title": str(config._meta.verbose_name_plural),
                "url": reverse("admin:visa_invitationletterorganizerconfig_changelist"),
            },
            {
                "title": str(config),
                "url": reverse(
                    "admin:visa_invitationletterorganizerconfig_change",
                    args=[config.id],
                ),
            },
            {
                "title": f"{str(document)} - Builder",
                "url": None,
            },
        ]


@admin.register(InvitationLetterOrganizerConfig)
class InvitationLetterOrganizerConfigAdmin(
    OrderedInlineModelAdminMixin, OrderedModelAdmin
):
    list_display = ("organizer",)
    search_fields = [
        "organizer__name",
    ]
    inlines = [InvitationLetterAssetInline, InvitationLetterDocumentInline]
