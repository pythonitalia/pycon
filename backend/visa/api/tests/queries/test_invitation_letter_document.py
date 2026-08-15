from django.contrib.auth.models import Permission
from visa.tests.factories import InvitationLetterDynamicDocumentFactory
import pytest

pytestmark = pytest.mark.django_db


def _invitation_letter_document(client, **input):
    return client.query(
        """query InvitationLetterDocument($id: ID!) {
        invitationLetterDocument(id: $id) {
            id
            dynamicDocument {
                header {
                    content
                }
                footer {
                    content
                }
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


def test_query_invitation_letter_document(admin_superuser, admin_graphql_api_client):
    admin_graphql_api_client.force_login(admin_superuser)

    document = InvitationLetterDynamicDocumentFactory()
    response = _invitation_letter_document(admin_graphql_api_client, id=document.id)

    assert response["data"]["invitationLetterDocument"]["id"] == str(document.id)
    assert response["data"]["invitationLetterDocument"]["dynamicDocument"] == {
        "header": {"content": "header"},
        "footer": {"content": "footer"},
        "pages": [
            {
                "id": "id",
                "title": "title",
                "content": "content",
            }
        ],
    }


def test_query_non_existent_invitation_letter_document(
    admin_superuser, admin_graphql_api_client
):
    admin_graphql_api_client.force_login(admin_superuser)

    InvitationLetterDynamicDocumentFactory()
    response = _invitation_letter_document(admin_graphql_api_client, id=959)
    assert not response.get("errors")
    assert not response["data"]["invitationLetterDocument"]


def test_query_non_existent_invitation_letter_document_as_user(
    user, admin_graphql_api_client
):
    admin_graphql_api_client.force_login(user)

    InvitationLetterDynamicDocumentFactory()
    response = _invitation_letter_document(admin_graphql_api_client, id=959)
    assert response["errors"][0]["message"] == "Cannot view invitation letter document"
    assert not response["data"]["invitationLetterDocument"]


def test_cannot_query_invitation_letter_document_as_user(
    user, admin_graphql_api_client
):
    admin_graphql_api_client.force_login(user)

    document = InvitationLetterDynamicDocumentFactory()
    response = _invitation_letter_document(admin_graphql_api_client, id=document.id)

    assert response["errors"][0]["message"] == "Cannot view invitation letter document"
    assert not response["data"]["invitationLetterDocument"]


def test_cannot_query_invitation_letter_document_as_staff_without_permission(
    admin_user, admin_graphql_api_client
):
    admin_graphql_api_client.force_login(admin_user)

    document = InvitationLetterDynamicDocumentFactory()

    response = _invitation_letter_document(admin_graphql_api_client, id=document.id)

    assert response["errors"][0]["message"] == "Cannot view invitation letter document"
    assert not response["data"]["invitationLetterDocument"]


def test_query_invitation_letter_document_as_staff(
    admin_user, admin_graphql_api_client
):
    admin_graphql_api_client.force_login(admin_user)

    document = InvitationLetterDynamicDocumentFactory()

    admin_user.admin_all_conferences = True
    admin_user.save()
    admin_user.user_permissions.add(
        Permission.objects.get(codename="view_invitationletterdocument")
    )

    response = _invitation_letter_document(admin_graphql_api_client, id=document.id)

    assert response["data"]["invitationLetterDocument"]["id"] == str(document.id)
