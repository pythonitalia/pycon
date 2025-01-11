from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Permission
from visa.tests.factories import (
    BASE_EXAMPLE_DYNAMIC_DOCUMENT_JSON,
    InvitationLetterDocumentFactory,
    InvitationLetterDynamicDocumentFactory,
)
import pytest

pytestmark = pytest.mark.django_db

NEW_DOC_GRAPHQL_INPUT = {
    "header": {"content": "new header", "margin": "0", "align": "top-left"},
    "footer": {
        "content": "new footer",
        "margin": "0",
        "align": "bottom-left",
    },
    "pageLayout": {"margin": "1cm 0 1cm 0"},
    "pages": [
        {
            "id": "id",
            "title": "new title",
            "content": "new content",
        }
    ],
}
NEW_DOC_JSON_DATA = {**NEW_DOC_GRAPHQL_INPUT}
NEW_DOC_JSON_DATA["page_layout"] = NEW_DOC_JSON_DATA.pop("pageLayout")

BASE_EXAMPLE_DYNAMIC_DOCUMENT_GRAPHQL_INPUT = {**BASE_EXAMPLE_DYNAMIC_DOCUMENT_JSON}
BASE_EXAMPLE_DYNAMIC_DOCUMENT_GRAPHQL_INPUT[
    "pageLayout"
] = BASE_EXAMPLE_DYNAMIC_DOCUMENT_GRAPHQL_INPUT.pop("page_layout")


def _update_invitation_letter_document(client, **input):
    return client.query(
        """mutation UpdateInvitationLetterDocument($input: UpdateInvitationLetterDocumentInput!) {
        updateInvitationLetterDocument(input: $input) {
            __typename
            ... on InvitationLetterDocument {
                id
                dynamicDocument {
                    header {
                        content
                        align
                        margin
                    }
                    footer {
                        content
                        align
                        margin
                    }
                    pageLayout {
                        margin
                    }
                    pages {
                        id
                        title
                        content
                    }
                }
            }
        }
    }""",
        variables=input,
    )


def test_update_invitation_letter_document(admin_superuser, admin_graphql_api_client):
    admin_graphql_api_client.force_login(admin_superuser)

    document = InvitationLetterDynamicDocumentFactory()

    response = _update_invitation_letter_document(
        admin_graphql_api_client,
        input={"id": document.id, "dynamicDocument": NEW_DOC_GRAPHQL_INPUT},
    )

    assert response["data"]["updateInvitationLetterDocument"]["id"] == str(document.id)
    assert (
        response["data"]["updateInvitationLetterDocument"]["dynamicDocument"]
        == NEW_DOC_GRAPHQL_INPUT
    )

    document.refresh_from_db()
    assert document.dynamic_document == NEW_DOC_JSON_DATA

    log_entry = LogEntry.objects.get()
    assert log_entry.object_id == str(document.invitation_letter_conference_config.id)


def test_update_invitation_letter_document_doesnt_record_in_log_empty_changes(
    admin_superuser, admin_graphql_api_client
):
    admin_graphql_api_client.force_login(admin_superuser)

    document = InvitationLetterDynamicDocumentFactory(
        dynamic_document=BASE_EXAMPLE_DYNAMIC_DOCUMENT_JSON
    )

    response = _update_invitation_letter_document(
        admin_graphql_api_client,
        input={
            "id": document.id,
            "dynamicDocument": BASE_EXAMPLE_DYNAMIC_DOCUMENT_GRAPHQL_INPUT,
        },
    )

    assert response["data"]["updateInvitationLetterDocument"]["id"] == str(document.id)
    assert (
        response["data"]["updateInvitationLetterDocument"]["dynamicDocument"]
        == BASE_EXAMPLE_DYNAMIC_DOCUMENT_GRAPHQL_INPUT
    )

    assert not LogEntry.objects.exists()

    document.refresh_from_db()
    assert document.dynamic_document == BASE_EXAMPLE_DYNAMIC_DOCUMENT_JSON


def test_cannot_update_invitation_letter_document_with_static_doc(
    admin_superuser, admin_graphql_api_client
):
    admin_graphql_api_client.force_login(admin_superuser)

    document = InvitationLetterDocumentFactory(dynamic_document=None)

    response = _update_invitation_letter_document(
        admin_graphql_api_client,
        input={"id": document.id, "dynamicDocument": NEW_DOC_GRAPHQL_INPUT},
    )

    assert (
        response["data"]["updateInvitationLetterDocument"]["__typename"]
        == "InvitationLetterDocumentNotEditable"
    )
    document.refresh_from_db()
    assert document.dynamic_document is None


def test_update_non_existent_invitation_letter_document(
    admin_superuser, admin_graphql_api_client
):
    admin_graphql_api_client.force_login(admin_superuser)

    document = InvitationLetterDocumentFactory(
        document=None,
        dynamic_document=BASE_EXAMPLE_DYNAMIC_DOCUMENT_JSON,
    )

    response = _update_invitation_letter_document(
        admin_graphql_api_client,
        input={"id": document.id + 1, "dynamicDocument": NEW_DOC_GRAPHQL_INPUT},
    )

    assert (
        response["data"]["updateInvitationLetterDocument"]["__typename"] == "NotFound"
    )

    document.refresh_from_db()
    assert document.dynamic_document == BASE_EXAMPLE_DYNAMIC_DOCUMENT_JSON


def test_update_invitation_letter_document_without_permission(admin_graphql_api_client):
    document = InvitationLetterDocumentFactory(
        document=None,
        dynamic_document=BASE_EXAMPLE_DYNAMIC_DOCUMENT_JSON,
    )

    response = _update_invitation_letter_document(
        admin_graphql_api_client,
        input={"id": document.id, "dynamicDocument": NEW_DOC_GRAPHQL_INPUT},
    )

    assert response["errors"][0]["message"] == "Cannot edit invitation letter document"
    document.refresh_from_db()
    assert document.dynamic_document == BASE_EXAMPLE_DYNAMIC_DOCUMENT_JSON


def test_update_invitation_letter_document_as_staff_without_permission(
    admin_user, admin_graphql_api_client
):
    admin_graphql_api_client.force_login(admin_user)

    document = InvitationLetterDocumentFactory(
        document=None,
        dynamic_document=BASE_EXAMPLE_DYNAMIC_DOCUMENT_JSON,
    )

    response = _update_invitation_letter_document(
        admin_graphql_api_client,
        input={"id": document.id, "dynamicDocument": NEW_DOC_GRAPHQL_INPUT},
    )

    assert response["errors"][0]["message"] == "Cannot edit invitation letter document"
    document.refresh_from_db()
    assert document.dynamic_document == BASE_EXAMPLE_DYNAMIC_DOCUMENT_JSON


def test_update_invitation_letter_document_as_staff_user_with_permission(
    admin_user, admin_graphql_api_client
):
    admin_graphql_api_client.force_login(admin_user)

    document = InvitationLetterDynamicDocumentFactory()

    admin_user.admin_all_conferences = True
    admin_user.save()
    admin_user.user_permissions.set(
        [
            Permission.objects.get(codename="change_invitationletterdocument"),
            Permission.objects.get(codename="view_invitationletterdocument"),
        ]
    )

    response = _update_invitation_letter_document(
        admin_graphql_api_client,
        input={"id": document.id, "dynamicDocument": NEW_DOC_GRAPHQL_INPUT},
    )

    assert response["data"]["updateInvitationLetterDocument"]["id"] == str(document.id)
    assert (
        response["data"]["updateInvitationLetterDocument"]["dynamicDocument"]
        == NEW_DOC_GRAPHQL_INPUT
    )

    document.refresh_from_db()
    assert document.dynamic_document == NEW_DOC_JSON_DATA
