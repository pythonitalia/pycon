from submissions.tests.factories import SubmissionFactory
from conferences.tests.factories import ConferenceFactory


def _upload_file(client, input):
    query = """
    mutation FileUpload($input: UploadFileInput!) {
        uploadFile(input: $input) {
            __typename
            ... on FileUploadRequest {
                id
                uploadUrl
                fields
            }
        }
    }
    """
    variables = {"input": input}
    return client.query(query, variables=variables)


def test_upload_participant_avatar_file(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory()
    response = _upload_file(
        graphql_client,
        {
            "participantAvatar": {
                "filename": "test.txt",
                "conferenceCode": conference.code,
            }
        },
    )

    id = response["data"]["uploadFile"]["id"]
    assert response["data"]["uploadFile"]["__typename"] == "FileUploadRequest"
    assert (
        response["data"]["uploadFile"]["uploadUrl"]
        == f"memory://files/participant_avatar/{id}.txt"
    )
    assert response["data"]["uploadFile"]["fields"] == '{"in-memory": true}'


def test_upload_proposal_resource_file(graphql_client, user):
    proposal = SubmissionFactory(speaker=user)
    graphql_client.force_login(user)

    response = _upload_file(
        graphql_client,
        {
            "proposalResource": {
                "filename": "test.txt",
                "proposalId": proposal.id,
            }
        },
    )

    id = response["data"]["uploadFile"]["id"]
    assert response["data"]["uploadFile"]["__typename"] == "FileUploadRequest"
    assert (
        response["data"]["uploadFile"]["uploadUrl"]
        == f"memory://files/proposal_resource/{id}.txt"
    )
    assert response["data"]["uploadFile"]["fields"] == '{"in-memory": true}'
