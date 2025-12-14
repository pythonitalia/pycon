import pytest
from uuid import uuid4
from users.tests.factories import UserFactory
from conferences.tests.factories import ConferenceFactory
from submissions.tests.factories import (
    ProposalMaterialFactory,
    SubmissionFactory,
    SubmissionTagFactory,
)
from files_upload.tests.factories import (
    FileFactory,
    ParticipantAvatarFileFactory,
    ProposalMaterialFileFactory,
)
from pytest import mark

from participants.models import Participant
from submissions.models import ProposalMaterial, Submission

pytestmark = mark.django_db


def _update_submission(
    graphql_client,
    *,
    submission,
    new_topic=None,
    new_audience=None,
    new_type=None,
    new_tag=None,
    new_duration=None,
    new_title=None,
    new_elevator_pitch=None,
    new_abstract=None,
    new_previous_talk_video="",
    new_speaker_level=Submission.SPEAKER_LEVELS.new,
    new_languages=["en"],
    new_short_social_summary="",
    new_speaker_bio="",
    new_speaker_photo=None,
    new_speaker_website="",
    new_speaker_twitter_handle="",
    new_instagram_handle="",
    new_speaker_linkedin_url="",
    new_speaker_facebook_url="",
    new_speaker_mastodon_handle="",
    new_speaker_availabilities=None,
    new_materials=None,
    new_do_not_record=None,
):
    new_topic = new_topic or submission.topic
    new_audience = new_audience or submission.audience_level
    new_type = new_type or submission.type
    new_tag = new_tag or submission.tags.first()
    new_duration = new_duration or submission.duration
    new_title = new_title or {"en": "new title to use"}
    new_elevator_pitch = new_elevator_pitch or {"en": "This is an elevator pitch"}
    new_abstract = new_abstract or {"en": "abstract here"}
    short_social_summary = new_short_social_summary or ""
    new_speaker_photo = new_speaker_photo or FileFactory().id
    new_speaker_availabilities = new_speaker_availabilities or {}
    new_materials = new_materials or []
    new_do_not_record = new_do_not_record or submission.do_not_record

    return graphql_client.query(
        """
    mutation Submission($input: UpdateSubmissionInput!) {
        updateSubmission(input: $input) {
            __typename

            ... on Submission {
                id
                title(language: "en")
                notes
                abstract(language: "en")
                elevatorPitch(language: "en")
                shortSocialSummary

                topic {
                    name
                    id
                }

                audienceLevel {
                    id
                    name
                }

                languages {
                    code
                }

                type {
                    id
                    name
                }

                tags {
                    name
                    id
                }

                conference {
                    id
                    name
                }

                duration {
                    id
                    name
                }

                speakerLevel
                previousTalkVideo
                doNotRecord
            }

            ... on SendSubmissionErrors {
                errors {
                    nonFieldErrors
                    validationTitle: title
                    validationNotes: notes
                    validationTopic: topic
                    validationAbstract: abstract
                    validationDuration: duration
                    validationAudienceLevel: audienceLevel
                    validationType: type
                    validationLanguages: languages
                    validationPreviousTalkVideo: previousTalkVideo
                    validationPreviousSpeakerLevel: speakerLevel
                    validationSpeakerBio: speakerBio
                    validationSpeakerPhoto: speakerPhoto
                    validationSpeakerWebsite: speakerWebsite
                    validationSpeakerTwitterHandle: speakerTwitterHandle
                    validationSpeakerInstagramHandle: speakerInstagramHandle
                    validationSpeakerLinkedinUrl: speakerLinkedinUrl
                    validationSpeakerFacebookUrl: speakerFacebookUrl
                    validationMaterials: materials {
                        fileId
                        url
                        id
                    }
                }
            }
        }
    }
    """,
        variables={
            "input": {
                "instance": submission.hashid,
                "title": new_title,
                "elevatorPitch": new_elevator_pitch,
                "abstract": new_abstract,
                "topic": new_topic.id,
                "audienceLevel": new_audience.id,
                "type": new_type.id,
                "languages": new_languages,
                "notes": "notes here",
                "tags": [new_tag.id],
                "duration": new_duration.id,
                "speakerLevel": new_speaker_level,
                "previousTalkVideo": new_previous_talk_video,
                "shortSocialSummary": short_social_summary,
                "speakerBio": new_speaker_bio,
                "speakerPhoto": new_speaker_photo,
                "speakerWebsite": new_speaker_website,
                "speakerTwitterHandle": new_speaker_twitter_handle,
                "speakerInstagramHandle": new_instagram_handle,
                "speakerLinkedinUrl": new_speaker_linkedin_url,
                "speakerFacebookUrl": new_speaker_facebook_url,
                "speakerMastodonHandle": new_speaker_mastodon_handle,
                "speakerAvailabilities": new_speaker_availabilities,
                "materials": new_materials,
                "doNotRecord": new_do_not_record,
            }
        },
    )


def test_update_submission(graphql_client, user):
    conference = ConferenceFactory(
        topics=("life", "diy"),
        languages=("it", "en"),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = SubmissionFactory(
        speaker_id=user.id,
        custom_topic="life",
        custom_duration="10m",
        custom_audience_level="adult",
        custom_submission_type="talk",
        languages=["it"],
        tags=["python", "ml"],
        conference=conference,
        speaker_level=Submission.SPEAKER_LEVELS.intermediate,
        previous_talk_video="https://www.youtube.com/watch?v=SlPhMPnQ58k",
    )

    graphql_client.force_login(user)

    new_topic = conference.topics.filter(name="diy").first()
    new_audience = conference.audience_levels.filter(name="senior").first()
    new_tag = SubmissionTagFactory(name="yello")
    new_duration = conference.durations.filter(name="20m").first()
    new_type = conference.submission_types.filter(name="workshop").first()

    response = _update_submission(
        graphql_client,
        submission=submission,
        new_topic=new_topic,
        new_audience=new_audience,
        new_tag=new_tag,
        new_duration=new_duration,
        new_type=new_type,
        new_speaker_level=Submission.SPEAKER_LEVELS.experienced,
        new_previous_talk_video="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        new_short_social_summary="test",
        new_speaker_facebook_url="http://facebook.com/pythonpizza",
        new_speaker_linkedin_url="http://linkedin.com/company/pythonpizza",
    )

    submission.refresh_from_db()

    assert response["data"]["updateSubmission"]["__typename"] == "Submission"

    participant = Participant.objects.first()
    assert participant.facebook_url == "http://facebook.com/pythonpizza"
    assert participant.linkedin_url == "http://linkedin.com/company/pythonpizza"


def test_update_submission_with_materials(graphql_client, user):
    conference = ConferenceFactory(
        topics=("life", "diy"),
        languages=("it", "en"),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = SubmissionFactory(
        speaker_id=user.id,
        custom_topic="life",
        custom_duration="10m",
        custom_audience_level="adult",
        custom_submission_type="talk",
        languages=["it"],
        tags=["python", "ml"],
        conference=conference,
        speaker_level=Submission.SPEAKER_LEVELS.intermediate,
        previous_talk_video="https://www.youtube.com/watch?v=SlPhMPnQ58k",
    )

    graphql_client.force_login(user)

    new_file = ProposalMaterialFileFactory(uploaded_by=user)
    response = _update_submission(
        graphql_client,
        submission=submission,
        new_materials=[
            {
                "fileId": new_file.id,
                "url": "",
                "name": "test.pdf",
            },
            {
                "fileId": None,
                "url": "https://www.google.com",
                "name": "https://www.google.com",
            },
        ],
    )

    submission.refresh_from_db()
    materials = submission.materials.order_by("id").all()

    assert len(materials) == 2
    assert materials[0].file_id == new_file.id
    assert materials[0].url == ""
    assert materials[0].name == "test.pdf"

    assert materials[1].file_id is None
    assert materials[1].url == "https://www.google.com"
    assert materials[1].name == "https://www.google.com"

    assert response["data"]["updateSubmission"]["__typename"] == "Submission"


def test_update_submission_with_existing_materials(graphql_client, user):
    conference = ConferenceFactory(
        topics=("life", "diy"),
        languages=("it", "en"),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = SubmissionFactory(
        speaker_id=user.id,
        custom_topic="life",
        custom_duration="10m",
        custom_audience_level="adult",
        custom_submission_type="talk",
        languages=["it"],
        tags=["python", "ml"],
        conference=conference,
        speaker_level=Submission.SPEAKER_LEVELS.intermediate,
        previous_talk_video="https://www.youtube.com/watch?v=SlPhMPnQ58k",
    )
    existing_material = ProposalMaterialFactory(
        proposal=submission, file=ProposalMaterialFileFactory(uploaded_by=user)
    )
    to_delete_material = ProposalMaterialFactory(
        proposal=submission, file=None, url="https://www.google.com"
    )

    graphql_client.force_login(user)

    new_file = ProposalMaterialFileFactory(uploaded_by=user)
    response = _update_submission(
        graphql_client,
        submission=submission,
        new_materials=[
            {
                "fileId": new_file.id,
                "url": "",
                "name": "test.pdf",
            },
            {
                "id": existing_material.id,
                "fileId": None,
                "url": "https://www.google.com",
                "name": "https://www.google.com",
            },
        ],
    )

    submission.refresh_from_db()
    materials = submission.materials.order_by("id").all()

    assert len(materials) == 2

    existing_material.refresh_from_db()

    assert existing_material.file_id is None
    assert existing_material.url == "https://www.google.com"
    assert existing_material.name == "https://www.google.com"

    assert response["data"]["updateSubmission"]["__typename"] == "Submission"

    assert not ProposalMaterial.objects.filter(id=to_delete_material.id).exists()


def test_update_submission_with_invalid_url(graphql_client, user):
    conference = ConferenceFactory(
        topics=("life", "diy"),
        languages=("it", "en"),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = SubmissionFactory(
        speaker_id=user.id,
        custom_topic="life",
        custom_duration="10m",
        custom_audience_level="adult",
        custom_submission_type="talk",
        languages=["it"],
        tags=["python", "ml"],
        conference=conference,
        speaker_level=Submission.SPEAKER_LEVELS.intermediate,
        previous_talk_video="https://www.youtube.com/watch?v=SlPhMPnQ58k",
    )

    graphql_client.force_login(user)

    response = _update_submission(
        graphql_client,
        submission=submission,
        new_materials=[
            {
                "fileId": None,
                "url": "invalid-url",
                "name": "test.pdf",
            },
        ],
    )

    assert response["data"]["updateSubmission"]["__typename"] == "SendSubmissionErrors"
    assert response["data"]["updateSubmission"]["errors"]["validationMaterials"][0][
        "url"
    ] == ["Invalid URL"]


def test_update_submission_with_other_submission_material(graphql_client, user):
    conference = ConferenceFactory(
        topics=("life", "diy"),
        languages=("it", "en"),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = SubmissionFactory(
        speaker_id=user.id,
        custom_topic="life",
        custom_duration="10m",
        custom_audience_level="adult",
        custom_submission_type="talk",
        languages=["it"],
        tags=["python", "ml"],
        conference=conference,
        speaker_level=Submission.SPEAKER_LEVELS.intermediate,
        previous_talk_video="https://www.youtube.com/watch?v=SlPhMPnQ58k",
    )
    other_submission_material = ProposalMaterialFactory(
        proposal=SubmissionFactory(conference=conference),
        file=ProposalMaterialFileFactory(uploaded_by=user),
    )

    graphql_client.force_login(user)

    response = _update_submission(
        graphql_client,
        submission=submission,
        new_materials=[
            {
                "id": other_submission_material.id,
                "fileId": None,
                "url": "https://www.google.com",
                "name": "https://www.google.com",
            },
        ],
    )

    assert response["data"]["updateSubmission"]["__typename"] == "SendSubmissionErrors"
    assert response["data"]["updateSubmission"]["errors"]["validationMaterials"][0][
        "id"
    ] == ["Material not found"]


def test_update_submission_with_invalid_material_id(graphql_client, user):
    conference = ConferenceFactory(
        topics=("life", "diy"),
        languages=("it", "en"),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = SubmissionFactory(
        speaker_id=user.id,
        custom_topic="life",
        custom_duration="10m",
        custom_audience_level="adult",
        custom_submission_type="talk",
        languages=["it"],
        tags=["python", "ml"],
        conference=conference,
        speaker_level=Submission.SPEAKER_LEVELS.intermediate,
        previous_talk_video="https://www.youtube.com/watch?v=SlPhMPnQ58k",
    )

    graphql_client.force_login(user)

    response = _update_submission(
        graphql_client,
        submission=submission,
        new_materials=[
            {
                "id": "invalid-id",
                "fileId": None,
                "url": "https://www.google.com",
                "name": "https://www.google.com",
            },
        ],
    )

    assert response["data"]["updateSubmission"]["__typename"] == "SendSubmissionErrors"
    assert response["data"]["updateSubmission"]["errors"]["validationMaterials"][0][
        "id"
    ] == ["Invalid material id"]


def test_update_submission_with_nonexistent_file_id(graphql_client, user):
    conference = ConferenceFactory(
        topics=("life", "diy"),
        languages=("it", "en"),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = SubmissionFactory(
        speaker_id=user.id,
        custom_topic="life",
        custom_duration="10m",
        custom_audience_level="adult",
        custom_submission_type="talk",
        languages=["it"],
        tags=["python", "ml"],
        conference=conference,
        speaker_level=Submission.SPEAKER_LEVELS.intermediate,
        previous_talk_video="https://www.youtube.com/watch?v=SlPhMPnQ58k",
    )

    graphql_client.force_login(user)

    response = _update_submission(
        graphql_client,
        submission=submission,
        new_materials=[
            {
                "fileId": uuid4(),
                "url": "",
                "name": "name",
            },
        ],
    )

    assert response["data"]["updateSubmission"]["__typename"] == "SendSubmissionErrors"
    assert response["data"]["updateSubmission"]["errors"]["validationMaterials"][0][
        "fileId"
    ] == ["File not found"]


def test_update_submission_with_file_from_different_user(graphql_client, user):
    conference = ConferenceFactory(
        topics=("life", "diy"),
        languages=("it", "en"),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = SubmissionFactory(
        speaker_id=user.id,
        custom_topic="life",
        custom_duration="10m",
        custom_audience_level="adult",
        custom_submission_type="talk",
        languages=["it"],
        tags=["python", "ml"],
        conference=conference,
        speaker_level=Submission.SPEAKER_LEVELS.intermediate,
        previous_talk_video="https://www.youtube.com/watch?v=SlPhMPnQ58k",
    )

    graphql_client.force_login(user)

    response = _update_submission(
        graphql_client,
        submission=submission,
        new_materials=[
            {
                "fileId": ProposalMaterialFileFactory(uploaded_by=UserFactory()).id,
                "url": "",
                "name": "name",
            },
        ],
    )

    assert response["data"]["updateSubmission"]["__typename"] == "SendSubmissionErrors"
    assert response["data"]["updateSubmission"]["errors"]["validationMaterials"][0][
        "fileId"
    ] == ["File not found"]


def test_update_submission_with_wrong_file_type(graphql_client, user):
    conference = ConferenceFactory(
        topics=("life", "diy"),
        languages=("it", "en"),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = SubmissionFactory(
        speaker_id=user.id,
        custom_topic="life",
        custom_duration="10m",
        custom_audience_level="adult",
        custom_submission_type="talk",
        languages=["it"],
        tags=["python", "ml"],
        conference=conference,
        speaker_level=Submission.SPEAKER_LEVELS.intermediate,
        previous_talk_video="https://www.youtube.com/watch?v=SlPhMPnQ58k",
    )

    graphql_client.force_login(user)

    response = _update_submission(
        graphql_client,
        submission=submission,
        new_materials=[
            {
                "fileId": ParticipantAvatarFileFactory(uploaded_by=user).id,
                "url": "",
                "name": "name",
            },
        ],
    )

    assert response["data"]["updateSubmission"]["__typename"] == "SendSubmissionErrors"
    assert response["data"]["updateSubmission"]["errors"]["validationMaterials"][0][
        "fileId"
    ] == ["File not found"]


def test_update_submission_with_too_long_url(graphql_client, user):
    conference = ConferenceFactory(
        topics=("life", "diy"),
        languages=("it", "en"),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = SubmissionFactory(
        speaker_id=user.id,
        custom_topic="life",
        custom_duration="10m",
        custom_audience_level="adult",
        custom_submission_type="talk",
        languages=["it"],
        tags=["python", "ml"],
        conference=conference,
        speaker_level=Submission.SPEAKER_LEVELS.intermediate,
        previous_talk_video="https://www.youtube.com/watch?v=SlPhMPnQ58k",
    )

    graphql_client.force_login(user)

    response = _update_submission(
        graphql_client,
        submission=submission,
        new_materials=[
            {
                "fileId": None,
                "url": f"https://www.googl{'e' * 2049}.com",
                "name": "name",
            },
        ],
    )

    assert response["data"]["updateSubmission"]["__typename"] == "SendSubmissionErrors"
    assert response["data"]["updateSubmission"]["errors"]["validationMaterials"][0][
        "url"
    ] == ["URL is too long"]


@pytest.mark.parametrize(
    "url",
    [
        "ftp://www.google.com",
        "//www.google.com",
        "google.com/test",
        "no/url",
    ],
)
def test_update_submission_with_invalid_urls(graphql_client, user, url):
    conference = ConferenceFactory(
        topics=("life", "diy"),
        languages=("it", "en"),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = SubmissionFactory(
        speaker_id=user.id,
        custom_topic="life",
        custom_duration="10m",
        custom_audience_level="adult",
        custom_submission_type="talk",
        languages=["it"],
        tags=["python", "ml"],
        conference=conference,
        speaker_level=Submission.SPEAKER_LEVELS.intermediate,
        previous_talk_video="https://www.youtube.com/watch?v=SlPhMPnQ58k",
    )

    graphql_client.force_login(user)

    response = _update_submission(
        graphql_client,
        submission=submission,
        new_materials=[
            {
                "fileId": None,
                "url": url,
                "name": "name",
            },
        ],
    )

    assert response["data"]["updateSubmission"]["__typename"] == "SendSubmissionErrors"
    assert response["data"]["updateSubmission"]["errors"]["validationMaterials"][0][
        "url"
    ] == ["Invalid URL"]


def test_update_submission_with_too_many_materials(graphql_client, user):
    conference = ConferenceFactory(
        topics=("life", "diy"),
        languages=("it", "en"),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = SubmissionFactory(
        speaker_id=user.id,
        custom_topic="life",
        custom_duration="10m",
        custom_audience_level="adult",
        custom_submission_type="talk",
        languages=["it"],
        tags=["python", "ml"],
        conference=conference,
        speaker_level=Submission.SPEAKER_LEVELS.intermediate,
        previous_talk_video="https://www.youtube.com/watch?v=SlPhMPnQ58k",
    )

    graphql_client.force_login(user)

    response = _update_submission(
        graphql_client,
        submission=submission,
        new_materials=[
            {
                "fileId": None,
                "url": "https://www.google.com",
                "name": "test.pdf",
            },
        ]
        * 4,
    )

    assert response["data"]["updateSubmission"]["__typename"] == "SendSubmissionErrors"
    assert response["data"]["updateSubmission"]["errors"]["nonFieldErrors"] == [
        "You can only add up to 3 materials"
    ]


def test_update_submission_speaker_availabilities(graphql_client, user):
    conference = ConferenceFactory(
        topics=("life", "diy"),
        languages=("it", "en"),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = SubmissionFactory(
        speaker_id=user.id,
        custom_topic="life",
        custom_duration="10m",
        custom_audience_level="adult",
        custom_submission_type="talk",
        languages=["it"],
        tags=["python", "ml"],
        conference=conference,
        speaker_level=Submission.SPEAKER_LEVELS.intermediate,
        previous_talk_video="https://www.youtube.com/watch?v=SlPhMPnQ58k",
    )

    graphql_client.force_login(user)

    new_topic = conference.topics.filter(name="diy").first()
    new_audience = conference.audience_levels.filter(name="senior").first()
    new_tag = SubmissionTagFactory(name="yello")
    new_duration = conference.durations.filter(name="20m").first()
    new_type = conference.submission_types.filter(name="workshop").first()

    response = _update_submission(
        graphql_client,
        submission=submission,
        new_topic=new_topic,
        new_audience=new_audience,
        new_tag=new_tag,
        new_duration=new_duration,
        new_type=new_type,
        new_speaker_level=Submission.SPEAKER_LEVELS.experienced,
        new_speaker_availabilities={
            "2023-12-10@am": "unavailable",
            "2023-12-11@pm": "unavailable",
            "2023-12-12@am": "preferred",
            "2023-12-13@am": None,
        },
    )

    submission.refresh_from_db()

    assert response["data"]["updateSubmission"]["__typename"] == "Submission"

    participant = Participant.objects.first()
    assert participant.speaker_availabilities == {
        "2023-12-10@am": "unavailable",
        "2023-12-11@pm": "unavailable",
        "2023-12-12@am": "preferred",
        "2023-12-13@am": None,
    }


def test_update_submission_with_invalid_facebook_social_url(graphql_client, user):
    conference = ConferenceFactory(
        topics=("life", "diy"),
        languages=("it", "en"),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = SubmissionFactory(
        speaker_id=user.id,
        custom_topic="life",
        custom_duration="10m",
        custom_audience_level="adult",
        custom_submission_type="talk",
        languages=["it"],
        tags=["python", "ml"],
        conference=conference,
        speaker_level=Submission.SPEAKER_LEVELS.intermediate,
        previous_talk_video="https://www.youtube.com/watch?v=SlPhMPnQ58k",
    )

    graphql_client.force_login(user)

    new_topic = conference.topics.filter(name="diy").first()
    new_audience = conference.audience_levels.filter(name="senior").first()
    new_tag = SubmissionTagFactory(name="yello")
    new_duration = conference.durations.filter(name="20m").first()
    new_type = conference.submission_types.filter(name="workshop").first()

    response = _update_submission(
        graphql_client,
        submission=submission,
        new_topic=new_topic,
        new_audience=new_audience,
        new_tag=new_tag,
        new_duration=new_duration,
        new_type=new_type,
        new_speaker_level=Submission.SPEAKER_LEVELS.experienced,
        new_previous_talk_video="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        new_short_social_summary="test",
        new_speaker_facebook_url="http://google.com/something-else",
    )

    submission.refresh_from_db()

    assert response["data"]["updateSubmission"]["__typename"] == "SendSubmissionErrors"
    assert response["data"]["updateSubmission"]["errors"][
        "validationSpeakerFacebookUrl"
    ] == ["Facebook URL should be a facebook.com link"]


def test_update_submission_with_invalid_linkedin_social_url(graphql_client, user):
    conference = ConferenceFactory(
        topics=("life", "diy"),
        languages=("it", "en"),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = SubmissionFactory(
        speaker_id=user.id,
        custom_topic="life",
        custom_duration="10m",
        custom_audience_level="adult",
        custom_submission_type="talk",
        languages=["it"],
        tags=["python", "ml"],
        conference=conference,
        speaker_level=Submission.SPEAKER_LEVELS.intermediate,
        previous_talk_video="https://www.youtube.com/watch?v=SlPhMPnQ58k",
    )

    graphql_client.force_login(user)

    new_topic = conference.topics.filter(name="diy").first()
    new_audience = conference.audience_levels.filter(name="senior").first()
    new_tag = SubmissionTagFactory(name="yello")
    new_duration = conference.durations.filter(name="20m").first()
    new_type = conference.submission_types.filter(name="workshop").first()

    response = _update_submission(
        graphql_client,
        submission=submission,
        new_topic=new_topic,
        new_audience=new_audience,
        new_tag=new_tag,
        new_duration=new_duration,
        new_type=new_type,
        new_speaker_level=Submission.SPEAKER_LEVELS.experienced,
        new_previous_talk_video="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        new_short_social_summary="test",
        new_speaker_linkedin_url="http://google.com/something-else",
    )

    submission.refresh_from_db()

    assert response["data"]["updateSubmission"]["__typename"] == "SendSubmissionErrors"
    assert response["data"]["updateSubmission"]["errors"][
        "validationSpeakerLinkedinUrl"
    ] == ["Linkedin URL should be a linkedin.com link"]


def test_update_submission_with_photo_to_upload(
    graphql_client,
    user,
):
    file = FileFactory()

    conference = ConferenceFactory(
        topics=("life", "diy"),
        languages=("it", "en"),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = SubmissionFactory(
        speaker_id=user.id,
        custom_topic="life",
        custom_duration="10m",
        custom_audience_level="adult",
        custom_submission_type="talk",
        languages=["it"],
        tags=["python", "ml"],
        conference=conference,
        speaker_level=Submission.SPEAKER_LEVELS.intermediate,
        previous_talk_video="https://www.youtube.com/watch?v=SlPhMPnQ58k",
    )

    graphql_client.force_login(user)

    new_topic = conference.topics.filter(name="diy").first()
    new_audience = conference.audience_levels.filter(name="senior").first()
    new_tag = SubmissionTagFactory(name="yello")
    new_duration = conference.durations.filter(name="20m").first()
    new_type = conference.submission_types.filter(name="workshop").first()

    response = _update_submission(
        graphql_client,
        submission=submission,
        new_topic=new_topic,
        new_audience=new_audience,
        new_tag=new_tag,
        new_duration=new_duration,
        new_type=new_type,
        new_speaker_level=Submission.SPEAKER_LEVELS.experienced,
        new_previous_talk_video="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        new_short_social_summary="test",
        new_speaker_photo=file.id,
    )

    submission.refresh_from_db()

    assert response["data"]["updateSubmission"]["__typename"] == "Submission"
    participant = Participant.objects.get(conference=conference, user_id=user.id)
    assert participant.photo_file_id == file.id


def test_cannot_update_submission_with_lang_outside_allowed_values(
    graphql_client, user
):
    conference = ConferenceFactory(
        topics=("life", "diy"),
        languages=("en",),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = SubmissionFactory(
        speaker_id=user.id,
        custom_topic="life",
        custom_duration="10m",
        custom_audience_level="adult",
        custom_submission_type="talk",
        languages=["it"],
        tags=["python", "ml"],
        conference=conference,
    )

    new_topic = conference.topics.filter(name="diy").first()
    new_audience = conference.audience_levels.filter(name="senior").first()
    new_tag = SubmissionTagFactory(name="yello")
    new_duration = conference.durations.filter(name="20m").first()
    new_type = conference.submission_types.filter(name="workshop").first()

    graphql_client.force_login(user)

    response = _update_submission(
        graphql_client,
        submission=submission,
        new_topic=new_topic,
        new_audience=new_audience,
        new_tag=new_tag,
        new_duration=new_duration,
        new_type=new_type,
        new_languages=["it"],
    )

    assert response["data"]["updateSubmission"]["__typename"] == "SendSubmissionErrors"

    assert response["data"]["updateSubmission"]["errors"]["validationLanguages"] == [
        "Language (it) is not allowed"
    ]


def test_can_edit_submission_outside_cfp(graphql_client, user):
    conference = ConferenceFactory(
        topics=("life", "diy"),
        languages=("en", "it"),
        durations=("10", "20"),
        active_cfp=False,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = SubmissionFactory(
        speaker_id=user.id,
        custom_topic="life",
        custom_duration="10m",
        custom_audience_level="adult",
        custom_submission_type="talk",
        languages=["en"],
        tags=["python", "ml"],
        conference=conference,
    )

    new_topic = conference.topics.filter(name="diy").first()
    new_audience = conference.audience_levels.filter(name="senior").first()
    new_tag = SubmissionTagFactory(name="yello")
    new_duration = conference.durations.filter(name="20m").first()
    new_type = conference.submission_types.filter(name="workshop").first()

    graphql_client.force_login(user)

    response = _update_submission(
        graphql_client,
        submission=submission,
        new_topic=new_topic,
        new_audience=new_audience,
        new_tag=new_tag,
        new_duration=new_duration,
        new_type=new_type,
        new_languages=["en"],
    )

    assert response["data"]["updateSubmission"]["__typename"] == "Submission"
    submission = Submission.objects.get(id=submission.id)
    assert list(submission.languages.values_list("code", flat=True)) == ["en"]


def test_cannot_edit_submission_if_not_the_owner(graphql_client, user):
    conference = ConferenceFactory(
        topics=("life", "diy"),
        languages=("en",),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = SubmissionFactory(
        custom_topic="life",
        custom_duration="10m",
        custom_audience_level="adult",
        custom_submission_type="talk",
        languages=["en"],
        tags=["python", "ml"],
        conference=conference,
    )

    new_topic = conference.topics.filter(name="diy").first()
    new_audience = conference.audience_levels.filter(name="senior").first()
    new_tag = SubmissionTagFactory(name="yello")
    new_duration = conference.durations.filter(name="20m").first()
    new_type = conference.submission_types.filter(name="workshop").first()

    graphql_client.force_login(user)

    response = _update_submission(
        graphql_client,
        submission=submission,
        new_topic=new_topic,
        new_audience=new_audience,
        new_tag=new_tag,
        new_duration=new_duration,
        new_type=new_type,
        new_languages=["en"],
    )

    assert response["data"]["updateSubmission"]["__typename"] == "SendSubmissionErrors"

    assert response["data"]["updateSubmission"]["errors"]["nonFieldErrors"] == [
        "You cannot edit this submission"
    ]


def test_make_submission_multi_lingual(graphql_client, user):
    conference = ConferenceFactory(
        topics=("life", "diy"),
        languages=("en", "it"),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = SubmissionFactory(
        speaker_id=user.id,
        custom_topic="life",
        custom_duration="10m",
        custom_audience_level="adult",
        custom_submission_type="talk",
        languages=["en"],
        tags=["python", "ml"],
        conference=conference,
        speaker_level=Submission.SPEAKER_LEVELS.intermediate,
        previous_talk_video="https://www.youtube.com/watch?v=SlPhMPnQ58k",
    )

    graphql_client.force_login(user)

    new_topic = conference.topics.filter(name="diy").first()
    new_audience = conference.audience_levels.filter(name="senior").first()
    new_tag = SubmissionTagFactory(name="yello")
    new_duration = conference.durations.filter(name="20m").first()
    new_type = conference.submission_types.filter(name="workshop").first()

    response = _update_submission(
        graphql_client,
        submission=submission,
        new_title={
            "en": "English",
            "it": "Italian",
        },
        new_elevator_pitch={
            "en": "Elevator English",
            "it": "Elevator Italian",
        },
        new_abstract={
            "en": "Abstract English",
            "it": "Abstract Italian",
        },
        new_topic=new_topic,
        new_audience=new_audience,
        new_tag=new_tag,
        new_duration=new_duration,
        new_type=new_type,
        new_speaker_level=Submission.SPEAKER_LEVELS.experienced,
        new_previous_talk_video="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        new_languages=["en", "it"],
    )

    assert response["data"]["updateSubmission"]["__typename"] == "Submission"

    submission.refresh_from_db()

    assert submission.title.localize("en") == "English"
    assert submission.title.localize("it") == "Italian"

    assert submission.elevator_pitch.localize("en") == "Elevator English"
    assert submission.elevator_pitch.localize("it") == "Elevator Italian"

    assert submission.abstract.localize("en") == "Abstract English"
    assert submission.abstract.localize("it") == "Abstract Italian"


def test_edit_submission_multi_lingual_fields_required(graphql_client, user):
    conference = ConferenceFactory(
        topics=("life", "diy"),
        languages=("en", "it"),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = SubmissionFactory(
        speaker_id=user.id,
        custom_topic="life",
        custom_duration="10m",
        custom_audience_level="adult",
        custom_submission_type="talk",
        languages=["en"],
        tags=["python", "ml"],
        conference=conference,
        speaker_level=Submission.SPEAKER_LEVELS.intermediate,
        previous_talk_video="https://www.youtube.com/watch?v=SlPhMPnQ58k",
    )

    graphql_client.force_login(user)

    new_topic = conference.topics.filter(name="diy").first()
    new_audience = conference.audience_levels.filter(name="senior").first()
    new_tag = SubmissionTagFactory(name="yello")
    new_duration = conference.durations.filter(name="20m").first()
    new_type = conference.submission_types.filter(name="workshop").first()

    response = _update_submission(
        graphql_client,
        submission=submission,
        new_title={
            "en": "English",
            "it": "",
        },
        new_elevator_pitch={
            "en": "Elevator English",
            "it": "",
        },
        new_abstract={
            "en": "Abstract English",
            "it": "",
        },
        new_topic=new_topic,
        new_audience=new_audience,
        new_tag=new_tag,
        new_duration=new_duration,
        new_type=new_type,
        new_speaker_level=Submission.SPEAKER_LEVELS.experienced,
        new_previous_talk_video="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        new_languages=["en", "it"],
    )

    submission.refresh_from_db()

    assert response["data"]["updateSubmission"]["__typename"] == "SendSubmissionErrors"
    assert response["data"]["updateSubmission"]["errors"]["validationAbstract"] == [
        "Italian: Cannot be empty"
    ]
    assert response["data"]["updateSubmission"]["errors"]["validationTitle"] == [
        "Italian: Cannot be empty"
    ]

    assert submission.languages.count() == 1


def test_update_submission_with_do_not_record_true(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("my-topic",),
        languages=("en", "it"),
        submission_types=("talk",),
        active_cfp=True,
        durations=("50",),
        audience_levels=("Beginner",),
    )

    submission = SubmissionFactory(
        speaker_id=user.id,
        conference=conference,
        do_not_record=False,
        tags=[
            "python",
        ],
    )

    graphql_client.force_login(user)

    response = _update_submission(
        graphql_client,
        submission=submission,
        new_do_not_record=True,
    )

    assert response["data"]["updateSubmission"]["__typename"] == "Submission"
    assert response["data"]["updateSubmission"]["doNotRecord"] is True

    submission.refresh_from_db()
    assert submission.do_not_record is True
