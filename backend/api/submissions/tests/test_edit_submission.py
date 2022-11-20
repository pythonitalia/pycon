import pytest
from pytest import mark

from participants.models import Participant
from submissions.models import Submission

pytestmark = mark.django_db


@pytest.fixture(autouse=True)
def change_azure_account_to_test_name(settings):
    settings.AZURE_STORAGE_ACCOUNT_NAME = "pytest-fakestorageaccount"


def _update_submission(
    graphql_client,
    *,
    submission,
    new_topic,
    new_audience,
    new_type,
    new_tag,
    new_duration,
    new_title=None,
    new_elevator_pitch=None,
    new_abstract=None,
    new_previous_talk_video="",
    new_speaker_level=Submission.SPEAKER_LEVELS.new,
    new_languages=["en"],
    new_short_social_summary="",
    new_speaker_bio="",
    new_speaker_photo="https://pytest-fakestorageaccount.blob.core.windows.net/participants-avatars/fake.jpg",
    new_speaker_website="",
    new_speaker_twitter_handle="",
    new_instagram_handle="",
    new_speaker_linkedin_url="",
    new_speaker_facebook_url="",
    new_speaker_mastodon_handle="",
):
    new_title = new_title or {"en": "new title to use"}
    new_elevator_pitch = new_elevator_pitch or {"en": "This is an elevator pitch"}
    new_abstract = new_abstract or {"en": "abstract here"}
    short_social_summary = new_short_social_summary or ""

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
            }

            ... on SendSubmissionErrors {
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
            }
        },
    )


def test_update_submission(
    graphql_client, user, conference_factory, submission_factory, submission_tag_factory
):
    conference = conference_factory(
        topics=("life", "diy"),
        languages=("it", "en"),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = submission_factory(
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
    new_tag = submission_tag_factory(name="yello")
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


def test_update_submission_with_invalid_facebook_social_url(
    graphql_client, user, conference_factory, submission_factory, submission_tag_factory
):
    conference = conference_factory(
        topics=("life", "diy"),
        languages=("it", "en"),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = submission_factory(
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
    new_tag = submission_tag_factory(name="yello")
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
    assert response["data"]["updateSubmission"]["validationSpeakerFacebookUrl"] == [
        "Facebook URL should be a facebook.com link"
    ]


def test_update_submission_with_invalid_linkedin_social_url(
    graphql_client, user, conference_factory, submission_factory, submission_tag_factory
):
    conference = conference_factory(
        topics=("life", "diy"),
        languages=("it", "en"),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = submission_factory(
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
    new_tag = submission_tag_factory(name="yello")
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
    assert response["data"]["updateSubmission"]["validationSpeakerLinkedinUrl"] == [
        "Linkedin URL should be a linkedin.com link"
    ]


def test_update_submission_with_photo_to_upload(
    graphql_client,
    user,
    conference_factory,
    submission_factory,
    submission_tag_factory,
    mocker,
):
    mock_confirm_upload = mocker.patch(
        "api.submissions.mutations.confirm_blob_upload_usage",
        return_value="https://pytest-fakestorageaccount.blob.core.windows.net/participants-avatars/my-photo.jpg",
    )

    speaker_photo = "https://pytest-fakestorageaccount.blob.core.windows.net/temporary-uploads/participants-avatars/my-photo.jpg"

    conference = conference_factory(
        topics=("life", "diy"),
        languages=("it", "en"),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = submission_factory(
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
    new_tag = submission_tag_factory(name="yello")
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
        new_speaker_photo=speaker_photo,
    )

    submission.refresh_from_db()
    mock_confirm_upload.assert_called()

    assert response["data"]["updateSubmission"]["__typename"] == "Submission"
    participant = Participant.objects.get(conference=conference, user_id=user.id)
    assert (
        participant.photo
        == "https://pytest-fakestorageaccount.blob.core.windows.net/participants-avatars/my-photo.jpg"
    )


def test_cannot_update_submission_with_lang_outside_allowed_values(
    graphql_client, user, conference_factory, submission_factory, submission_tag_factory
):
    conference = conference_factory(
        topics=("life", "diy"),
        languages=("en",),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = submission_factory(
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
    new_tag = submission_tag_factory(name="yello")
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

    assert response["data"]["updateSubmission"]["validationLanguages"] == [
        "Language (it) is not allowed"
    ]


def test_can_edit_submission_outside_cfp(
    graphql_client, user, conference_factory, submission_factory, submission_tag_factory
):
    conference = conference_factory(
        topics=("life", "diy"),
        languages=("en", "it"),
        durations=("10", "20"),
        active_cfp=False,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = submission_factory(
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
    new_tag = submission_tag_factory(name="yello")
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


def test_cannot_edit_submission_if_not_the_owner(
    graphql_client, user, conference_factory, submission_factory, submission_tag_factory
):
    conference = conference_factory(
        topics=("life", "diy"),
        languages=("en",),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = submission_factory(
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
    new_tag = submission_tag_factory(name="yello")
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

    assert response["data"]["updateSubmission"]["nonFieldErrors"] == [
        "You cannot edit this submission"
    ]


def test_make_submission_multi_lingual(
    graphql_client, user, conference_factory, submission_factory, submission_tag_factory
):
    conference = conference_factory(
        topics=("life", "diy"),
        languages=("en", "it"),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = submission_factory(
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
    new_tag = submission_tag_factory(name="yello")
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


def test_edit_submission_multi_lingual_fields_required(
    graphql_client, user, conference_factory, submission_factory, submission_tag_factory
):
    conference = conference_factory(
        topics=("life", "diy"),
        languages=("en", "it"),
        durations=("10", "20"),
        active_cfp=True,
        audience_levels=("adult", "senior"),
        submission_types=("talk", "workshop"),
    )

    submission = submission_factory(
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
    new_tag = submission_tag_factory(name="yello")
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
    assert response["data"]["updateSubmission"]["validationAbstract"] == [
        "Italian: Cannot be empty"
    ]
    assert response["data"]["updateSubmission"]["validationTitle"] == [
        "Italian: Cannot be empty"
    ]

    assert submission.languages.count() == 1
