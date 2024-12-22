from django.urls import reverse
from django.contrib.admin.sites import AdminSite
from visa.models import InvitationLetterConferenceConfig, InvitationLetterRequest
from visa.admin import InvitationLetterDocumentInline, InvitationLetterRequestAdmin
import pytest

from visa.tests.factories import (
    InvitationLetterDocumentFactory,
    InvitationLetterConferenceConfigFactory,
    InvitationLetterRequestFactory,
)

pytestmark = pytest.mark.django_db


def test_edit_dynamic_document_view(rf, admin_user):
    admin = InvitationLetterDocumentInline(
        parent_model=InvitationLetterConferenceConfig, admin_site=AdminSite()
    )

    config = InvitationLetterConferenceConfigFactory()
    document = InvitationLetterDocumentFactory(
        invitation_letter_conference_config=config,
        document=None,
    )

    request = rf.get("/")
    request.user = admin_user
    response = admin.edit_dynamic_document_view(request, config.id, document.id)

    assert response.status_code == 200
    assert response.template_name == "astro/invitation-letter-document-builder.html"
    assert response.context_data["document_id"] == document.id
    assert response.context_data["breadcrumbs"]


def test_edit_dynamic_document_button():
    admin = InvitationLetterDocumentInline(
        parent_model=InvitationLetterConferenceConfig, admin_site=AdminSite()
    )

    config = InvitationLetterConferenceConfigFactory()
    document = InvitationLetterDocumentFactory(
        invitation_letter_conference_config=config,
        document=None,
    )

    html = admin.edit_dynamic_document(document)

    url = reverse(
        "admin:edit_dynamic_document",
        kwargs={
            "config_id": config.id,
            "document_id": document.id,
        },
    )
    assert html == f'<a href="{url}">Edit</a>'


def test_edit_dynamic_document_button_is_empty_for_static_docs():
    admin = InvitationLetterDocumentInline(
        parent_model=InvitationLetterConferenceConfig, admin_site=AdminSite()
    )

    config = InvitationLetterConferenceConfigFactory()
    document = InvitationLetterDocumentFactory(
        invitation_letter_conference_config=config
    )

    html = admin.edit_dynamic_document(document)

    assert html == ""


def test_invitation_letter_request_admin():
    admin = InvitationLetterRequestAdmin(
        model=InvitationLetterRequest, admin_site=AdminSite()
    )

    invitation_letter_request = InvitationLetterRequestFactory()

    assert 'name="_process_now"' in admin.process_now(invitation_letter_request)
    assert "Generate the invitation letter first" == admin.send_via_email(
        invitation_letter_request
    )


def test_invitation_letter_request_admin_post_processing_redirects_to_changelist(
    rf, admin_user
):
    admin = InvitationLetterRequestAdmin(
        model=InvitationLetterRequest, admin_site=AdminSite()
    )

    invitation_letter_request = InvitationLetterRequestFactory()
    request = rf.post("/")
    request.user = admin_user
    request.POST = {"_process_now": "1"}
    response = admin.response_post_save_change(request, invitation_letter_request)

    assert response.status_code == 302
    assert response.url == reverse(
        "admin:visa_invitationletterrequest_change", args=[invitation_letter_request.id]
    )
