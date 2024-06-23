import pytest
from files_upload.models import File
from submissions.tests.factories import SubmissionFactory
from conferences.tests.factories import ConferenceFactory
from django.test import override_settings


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


def test_upload_participant_avatar_to_invalid_conf_fails(graphql_client, user):
    graphql_client.force_login(user)

    ConferenceFactory()
    response = _upload_file(
        graphql_client,
        {
            "participantAvatar": {
                "filename": "test.txt",
                "conferenceCode": "aee",
            }
        },
    )

    assert not response["data"]
    assert response["errors"][0]["message"] == "You cannot upload files of this type"


def test_upload_proposal_material_file(graphql_client, user):
    proposal = SubmissionFactory(speaker=user)
    graphql_client.force_login(user)

    response = _upload_file(
        graphql_client,
        {
            "proposalMaterial": {
                "filename": "test.txt",
                "proposalId": proposal.hashid,
                "conferenceCode": proposal.conference.code,
            }
        },
    )

    id = response["data"]["uploadFile"]["id"]
    assert response["data"]["uploadFile"]["__typename"] == "FileUploadRequest"
    assert (
        response["data"]["uploadFile"]["uploadUrl"]
        == f"memory://files/proposal_material/{id}.txt"
    )
    assert response["data"]["uploadFile"]["fields"] == '{"in-memory": true}'


def test_cannot_upload_proposal_material_file_if_not_speaker(graphql_client, user):
    proposal = SubmissionFactory()
    graphql_client.force_login(user)

    response = _upload_file(
        graphql_client,
        {
            "proposalMaterial": {
                "filename": "test.txt",
                "proposalId": proposal.hashid,
                "conferenceCode": proposal.conference.code,
            }
        },
    )

    assert not response["data"]
    assert response["errors"][0]["message"] == "You cannot upload files of this type"


def test_cannot_upload_proposal_material_file_with_invalid_proposal_id(
    graphql_client, user
):
    graphql_client.force_login(user)

    response = _upload_file(
        graphql_client,
        {
            "proposalMaterial": {
                "filename": "test.txt",
                "proposalId": "abcabc",
                "conferenceCode": ConferenceFactory().code,
            }
        },
    )

    assert not response["data"]
    assert response["errors"][0]["message"] == "You cannot upload files of this type"


def test_cannot_upload_proposal_material_file_with_invalid_proposal_id_for_conference(
    graphql_client, user
):
    proposal = SubmissionFactory()
    graphql_client.force_login(user)

    response = _upload_file(
        graphql_client,
        {
            "proposalMaterial": {
                "filename": "test.txt",
                "proposalId": proposal.hashid,
                "conferenceCode": ConferenceFactory().code,
            }
        },
    )

    assert not response["data"]
    assert response["errors"][0]["message"] == "You cannot upload files of this type"


@pytest.mark.parametrize(
    "file_type", [File.Type.PARTICIPANT_AVATAR, File.Type.PROPOSAL_MATERIAL]
)
def test_superusers_can_upload_anything(graphql_client, admin_superuser, file_type):
    proposal = SubmissionFactory()
    graphql_client.force_login(admin_superuser)

    req_input = {}
    match file_type:
        case File.Type.PARTICIPANT_AVATAR:
            req_input["participantAvatar"] = {
                "filename": "test.txt",
                "conferenceCode": "random",
            }
        case File.Type.PROPOSAL_MATERIAL:
            req_input["proposalMaterial"] = {
                "filename": "test.txt",
                "proposalId": proposal.hashid,
                "conferenceCode": proposal.conference.code,
            }

    response = _upload_file(
        graphql_client,
        req_input,
    )

    assert not response.get("errors")
    assert response["data"]["uploadFile"]["__typename"] == "FileUploadRequest"


@override_settings(
    CACHES={
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique",
        }
    }
)
def test_file_upload_is_rate_limited(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory()
    for _ in range(20):
        response = _upload_file(
            graphql_client,
            {
                "participantAvatar": {
                    "filename": "test.txt",
                    "conferenceCode": conference.code,
                }
            },
        )

    assert not response["data"]
    assert response["errors"][0]["message"] == "Rate limit exceeded."
    assert File.objects.count() == 10
