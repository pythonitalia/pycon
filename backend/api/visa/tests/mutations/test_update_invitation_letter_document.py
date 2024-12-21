from django.contrib.auth.models import Permission
from conferences.tests.factories import ConferenceFactory
from visa.tests.factories import InvitationLetterDocumentFactory
import pytest

pytestmark = pytest.mark.django_db


def _update_invitation_letter_document(client, **input):
    return client.query(
        """mutation UpdateInvitationLetterDocument($input: UpdateInvitationLetterDocumentInput!) {
        updateInvitationLetterDocument(input: $input) {
            id
            dynamicDocument {
                header
                footer
                pages {
                    id
                    title
                    content
                }
            }
        }
    }""",
        variables=input,
    )


def test_update_invitation_letter_document(admin_superuser, admin_graphql_api_client):
    admin_graphql_api_client.force_login(admin_superuser)

    document = InvitationLetterDocumentFactory(
        document=None,
        dynamic_document={
            "header": "header",
            "footer": "footer",
            "pages": [
                {
                    "id": "id",
                    "title": "title",
                    "content": "content",
                }
            ],
        },
    )

    response = _update_invitation_letter_document(
        admin_graphql_api_client,
        input={
            "id": document.id,
            "dynamicDocument": {
                "header": "new header",
                "footer": "new footer",
                "pages": [
                    {
                        "id": "id",
                        "title": "new title",
                        "content": "new content",
                    }
                ],
            },
        },
    )

    assert response["data"]["updateInvitationLetterDocument"]["id"] == str(document.id)
    assert response["data"]["updateInvitationLetterDocument"]["dynamicDocument"] == {
        "header": "new header",
        "footer": "new footer",
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
        "header": "new header",
        "footer": "new footer",
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
        input={
            "id": document.id,
            "dynamicDocument": {
                "header": "new header",
                "footer": "new footer",
                "pages": [
                    {
                        "id": "id",
                        "title": "new title",
                        "content": "new content",
                    }
                ],
            },
        },
    )

    assert (
        response["errors"][0]["message"]
        == "Invitation letter document has a file attached"
    )
    document.refresh_from_db()
    assert document.dynamic_document is None


def test_update_non_existent_invitation_letter_document(
    admin_superuser, admin_graphql_api_client
):
    admin_graphql_api_client.force_login(admin_superuser)

    document = InvitationLetterDocumentFactory(
        document=None,
        dynamic_document={
            "header": "header",
            "footer": "footer",
            "pages": [
                {
                    "id": "id",
                    "title": "title",
                    "content": "content",
                }
            ],
        },
    )

    response = _update_invitation_letter_document(
        admin_graphql_api_client,
        input={
            "id": document.id + 1,
            "dynamicDocument": {
                "header": "new header",
                "footer": "new footer",
                "pages": [
                    {
                        "id": "id",
                        "title": "new title",
                        "content": "new content",
                    }
                ],
            },
        },
    )

    assert response["errors"][0]["message"] == "Invitation letter document not found"
    document.refresh_from_db()
    assert document.dynamic_document == {
        "header": "header",
        "footer": "footer",
        "pages": [
            {
                "id": "id",
                "title": "title",
                "content": "content",
            }
        ],
    }


def test_update_invitation_letter_document_without_permission(admin_graphql_api_client):
    document = InvitationLetterDocumentFactory(
        document=None,
        dynamic_document={
            "header": "header",
            "footer": "footer",
            "pages": [
                {
                    "id": "id",
                    "title": "title",
                    "content": "content",
                }
            ],
        },
    )

    response = _update_invitation_letter_document(
        admin_graphql_api_client,
        input={
            "id": document.id,
            "dynamicDocument": {
                "header": "new header",
                "footer": "new footer",
                "pages": [
                    {
                        "id": "id",
                        "title": "new title",
                        "content": "new content",
                    }
                ],
            },
        },
    )

    assert response["errors"][0]["message"] == "Cannot edit invitation letter document"
    document.refresh_from_db()
    assert document.dynamic_document == {
        "header": "header",
        "footer": "footer",
        "pages": [
            {
                "id": "id",
                "title": "title",
                "content": "content",
            }
        ],
    }


def test_update_invitation_letter_document_as_staff_without_permission(
    admin_user, admin_graphql_api_client
):
    admin_graphql_api_client.force_login(admin_user)

    document = InvitationLetterDocumentFactory(
        document=None,
        dynamic_document={
            "header": "header",
            "footer": "footer",
            "pages": [
                {
                    "id": "id",
                    "title": "title",
                    "content": "content",
                }
            ],
        },
    )
    ConferenceFactory(organizer=document.invitation_letter_organizer_config.organizer)

    response = _update_invitation_letter_document(
        admin_graphql_api_client,
        input={
            "id": document.id,
            "dynamicDocument": {
                "header": "new header",
                "footer": "new footer",
                "pages": [
                    {
                        "id": "id",
                        "title": "new title",
                        "content": "new content",
                    }
                ],
            },
        },
    )

    assert response["errors"][0]["message"] == "Cannot edit invitation letter document"
    document.refresh_from_db()
    assert document.dynamic_document == {
        "header": "header",
        "footer": "footer",
        "pages": [
            {
                "id": "id",
                "title": "title",
                "content": "content",
            }
        ],
    }


def test_update_invitation_letter_document_as_staff_user_with_permission(
    admin_user, admin_graphql_api_client
):
    admin_graphql_api_client.force_login(admin_user)

    document = InvitationLetterDocumentFactory(
        document=None,
        dynamic_document={
            "header": "header",
            "footer": "footer",
            "pages": [
                {
                    "id": "id",
                    "title": "title",
                    "content": "content",
                }
            ],
        },
    )
    ConferenceFactory(organizer=document.invitation_letter_organizer_config.organizer)

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
        input={
            "id": document.id,
            "dynamicDocument": {
                "header": "new header",
                "footer": "new footer",
                "pages": [
                    {
                        "id": "id",
                        "title": "new title",
                        "content": "new content",
                    }
                ],
            },
        },
    )

    assert response["data"]["updateInvitationLetterDocument"]["id"] == str(document.id)
    assert response["data"]["updateInvitationLetterDocument"]["dynamicDocument"] == {
        "header": "new header",
        "footer": "new footer",
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
        "header": "new header",
        "footer": "new footer",
        "pages": [
            {
                "id": "id",
                "title": "new title",
                "content": "new content",
            }
        ],
    }
