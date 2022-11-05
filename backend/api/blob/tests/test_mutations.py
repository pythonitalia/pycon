import pytest

from blob.enum import BlobContainer
from blob.upload import BlobUpload

pytestmark = pytest.mark.django_db


def test_fetch_with_empty_checklist_items(graphql_client, mocker, user):
    graphql_client.force_login(user)
    mocker.patch("api.blob.mutations.uuid4", return_value="123")
    mock_create_blob_upload = mocker.patch(
        "api.blob.mutations.create_blob_upload",
        return_value=BlobUpload(
            upload_url="http://blob.upload.csw?token=123",
            file_url="http://blob.upload.csw",
        ),
    )
    response = graphql_client.query(
        """mutation {
            generateParticipantAvatarUploadUrl {
                uploadUrl
                fileUrl
            }
        }"""
    )

    mock_create_blob_upload.assert_called_with(
        BlobContainer.PARTICIPANTS_AVATARS, "123.jpg"
    )

    assert not response.get("errors")
    assert response["data"]["generateParticipantAvatarUploadUrl"] == {
        "uploadUrl": "http://blob.upload.csw?token=123",
        "fileUrl": "http://blob.upload.csw",
    }
