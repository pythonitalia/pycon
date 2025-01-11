from django.contrib.auth.models import Permission
from visa.tests.factories import (
    InvitationLetterDocumentFactory,
    InvitationLetterDynamicDocumentFactory,
)
import pytest

pytestmark = pytest.mark.django_db

NEW_DOC_PAYLOAD_EXAMPLE = {
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
NEW_DOC_JSON_PAYLOAD_EXAMPLE = {
    **NEW_DOC_PAYLOAD_EXAMPLE,
    "page_layout": NEW_DOC_PAYLOAD_EXAMPLE.get("pageLayout"),
}
NEW_DOC_JSON_PAYLOAD_EXAMPLE.pop("pageLayout")


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
        input={"id": document.id, "dynamicDocument": NEW_DOC_PAYLOAD_EXAMPLE},
    )

    assert response["data"]["updateInvitationLetterDocument"]["id"] == str(document.id)
    assert response["data"]["updateInvitationLetterDocument"]["dynamicDocument"] == {
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

    document.refresh_from_db()
    assert document.dynamic_document == {
        "header": {"content": "new header", "margin": "0", "align": "top-left"},
        "footer": {"content": "new footer", "margin": "0", "align": "bottom-left"},
        "page_layout": {"margin": "1cm 0 1cm 0"},
        "pages": [
            {
                "id": "id",
                "title": "new title",
                "content": "new content",
            }
        ],
    }


def test_cannot_update_invitation_letter_document_with_static_doc(
    admin_superuser, admin_graphql_api_client
):
    admin_graphql_api_client.force_login(admin_superuser)

    document = InvitationLetterDocumentFactory(dynamic_document=None)

    response = _update_invitation_letter_document(
        admin_graphql_api_client,
        input={"id": document.id, "dynamicDocument": NEW_DOC_PAYLOAD_EXAMPLE},
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
    old_doc = {
        "header": {"content": "new header", "align": "top-left"},
        "footer": {"content": "new footer", "align": "bottom-left"},
        "pageLayout": {"margin": "1cm 0 1cm 0"},
        "pages": [
            {
                "id": "id",
                "title": "title",
                "content": "content",
            }
        ],
    }
    document = InvitationLetterDocumentFactory(
        document=None,
        dynamic_document=old_doc,
    )

    response = _update_invitation_letter_document(
        admin_graphql_api_client,
        input={"id": document.id + 1, "dynamicDocument": NEW_DOC_PAYLOAD_EXAMPLE},
    )

    assert (
        response["data"]["updateInvitationLetterDocument"]["__typename"] == "NotFound"
    )

    document.refresh_from_db()
    assert document.dynamic_document == old_doc


def test_update_invitation_letter_document_without_permission(admin_graphql_api_client):
    old_doc = {
        "header": {"content": "header", "align": "top-left"},
        "footer": {"content": "footer", "align": "bottom-left"},
        "pageLayout": {"margin": "1cm 0 1cm 0"},
        "pages": [
            {
                "id": "id",
                "title": "title",
                "content": "content",
            }
        ],
    }
    document = InvitationLetterDocumentFactory(
        document=None,
        dynamic_document=old_doc,
    )

    response = _update_invitation_letter_document(
        admin_graphql_api_client,
        input={"id": document.id, "dynamicDocument": NEW_DOC_PAYLOAD_EXAMPLE},
    )

    assert response["errors"][0]["message"] == "Cannot edit invitation letter document"
    document.refresh_from_db()
    assert document.dynamic_document == old_doc


def test_update_invitation_letter_document_as_staff_without_permission(
    admin_user, admin_graphql_api_client
):
    admin_graphql_api_client.force_login(admin_user)
    old_doc = {
        "header": {"content": "header", "align": "top-left"},
        "footer": {"content": "footer", "align": "bottom-left"},
        "pageLayout": {"margin": "1cm 0 1cm 0"},
        "pages": [
            {
                "id": "id",
                "title": "title",
                "content": "content",
            }
        ],
    }

    document = InvitationLetterDocumentFactory(
        document=None,
        dynamic_document=old_doc,
    )

    response = _update_invitation_letter_document(
        admin_graphql_api_client,
        input={"id": document.id, "dynamicDocument": NEW_DOC_PAYLOAD_EXAMPLE},
    )

    assert response["errors"][0]["message"] == "Cannot edit invitation letter document"
    document.refresh_from_db()
    assert document.dynamic_document == old_doc


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
        input={"id": document.id, "dynamicDocument": NEW_DOC_PAYLOAD_EXAMPLE},
    )

    assert response["data"]["updateInvitationLetterDocument"]["id"] == str(document.id)
    assert (
        response["data"]["updateInvitationLetterDocument"]["dynamicDocument"]
        == NEW_DOC_PAYLOAD_EXAMPLE
    )

    document.refresh_from_db()
    assert document.dynamic_document == NEW_DOC_JSON_PAYLOAD_EXAMPLE
