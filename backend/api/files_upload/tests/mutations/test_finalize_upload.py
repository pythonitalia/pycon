from celery.exceptions import TimeoutError
from uuid import uuid4
from users.tests.factories import UserFactory
from files_upload.tests.factories import FileFactory


def _finalize_upload(client, input):
    query = """
    mutation FinalizeUpload($input: FinalizeUploadInput!) {
        finalizeUpload(input: $input) {
            __typename
            id
            virus
            mimeType
        }
    }
    """
    variables = {"input": input}
    return client.query(query, variables=variables)


def test_finalize_upload(graphql_client, user, mocker):
    mock_task = mocker.patch(
        "api.files_upload.mutations.finalize_upload.post_process_file_upload"
    )

    graphql_client.force_login(user)
    file = FileFactory(uploaded_by=user)

    response = _finalize_upload(graphql_client, {"fileId": file.id})

    mock_task.delay.assert_called()
    assert not response.get("errors")
    assert response["data"]["finalizeUpload"]["id"] == str(file.id)


def test_finalize_upload_when_the_task_takes_too_long(graphql_client, user, mocker):
    mock_task = mocker.patch(
        "api.files_upload.mutations.finalize_upload.post_process_file_upload"
    )
    mock_task.delay.return_value.get.side_effect = TimeoutError

    graphql_client.force_login(user)
    file = FileFactory(uploaded_by=user)

    response = _finalize_upload(graphql_client, {"fileId": file.id})

    mock_task.delay.assert_called()
    assert not response.get("errors")
    assert response["data"]["finalizeUpload"]["id"] == str(file.id)


def test_cannot_finalize_other_user_file(graphql_client, user, mocker):
    mock_task = mocker.patch(
        "api.files_upload.mutations.finalize_upload.post_process_file_upload"
    )

    graphql_client.force_login(user)
    file = FileFactory(uploaded_by=UserFactory())

    response = _finalize_upload(graphql_client, {"fileId": file.id})

    mock_task.delay.assert_not_called()
    assert response["errors"][0]["message"] == "File not found"
    assert response["data"] is None


def test_finalize_with_invalid_id(graphql_client, user, mocker):
    mock_task = mocker.patch(
        "api.files_upload.mutations.finalize_upload.post_process_file_upload"
    )

    graphql_client.force_login(user)
    FileFactory(uploaded_by=user)

    response = _finalize_upload(graphql_client, {"fileId": uuid4()})

    mock_task.delay.assert_not_called()
    assert response["errors"][0]["message"] == "File not found"
    assert response["data"] is None


def test_finalize_upload_of_already_processed_file_is_ignored(
    graphql_client, user, mocker
):
    mock_task = mocker.patch(
        "api.files_upload.mutations.finalize_upload.post_process_file_upload"
    )

    graphql_client.force_login(user)
    file = FileFactory(uploaded_by=user)
    file.virus = True
    file.save()

    response = _finalize_upload(graphql_client, {"fileId": file.id})

    mock_task.delay.assert_not_called()
    assert not response.get("errors")
    assert response["data"]["finalizeUpload"]["id"] == str(file.id)
