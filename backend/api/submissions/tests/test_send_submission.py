from notifications.models import EmailTemplateIdentifier
from notifications.tests.factories import EmailTemplateFactory
from privacy_policy.models import PrivacyPolicyAcceptanceRecord
from files_upload.tests.factories import FileFactory
from conferences.tests.factories import (
    AudienceLevelFactory,
    ConferenceFactory,
    DurationFactory,
    TopicFactory,
)
from pytest import mark

from participants.models import Participant
from submissions.models import Submission, SubmissionTag, SubmissionType
from submissions.tests.factories import SubmissionFactory, SubmissionTypeFactory

pytestmark = mark.django_db


def _submit_talk(client, conference, **kwargs):
    talk = SubmissionFactory.build(
        type=SubmissionType.objects.get_or_create(name="talk")[0]
    )

    return _submit_proposal(client, conference, submission=talk, **kwargs)


def _submit_tutorial(client, conference, **kwargs):
    workshop = SubmissionFactory.create(
        type=SubmissionType.objects.get_or_create(name="tutorial")[0]
    )

    return _submit_proposal(client, conference, submission=workshop, **kwargs)


def _submit_proposal(client, conference, submission, **kwargs):
    languages = [language.code for language in conference.languages.all()]
    tag, _ = SubmissionTag.objects.get_or_create(name="tag")

    defaults = {
        "title": {
            "en": submission.title.data.get("en", ""),
            "it": submission.title.data.get("it", ""),
        },
        "abstract": {
            "en": submission.abstract.data.get("en", ""),
            "it": submission.abstract.data.get("it", ""),
        },
        "elevatorPitch": {
            "en": submission.elevator_pitch.data.get("en", ""),
            "it": submission.elevator_pitch.data.get("it", ""),
        },
        "notes": submission.notes,
        "languages": languages,
        "conference": conference.code,
        "topic": conference.topics.first().id,
        "type": submission.type.id,
        "duration": conference.durations.first().id,
        "audienceLevel": conference.audience_levels.first().id,
        "speakerLevel": submission.speaker_level,
        "previousTalkVideo": submission.previous_talk_video,
        "shortSocialSummary": "",
        "speakerBio": "bio",
        "speakerPhoto": FileFactory().id,
        "speakerWebsite": "http://website.it",
        "speakerTwitterHandle": "handle",
        "speakerInstagramHandle": "handleinsta",
        "speakerLinkedinUrl": "https://linkedin.com/fake-link",
        "speakerFacebookUrl": "https://facebook.com/fake-link",
        "speakerMastodonHandle": "fake@mastodon.social",
        "tags": [tag.id],
        "speakerAvailabilities": {},
    }

    override_conference = kwargs.pop("override_conference", None)

    variables = {
        **defaults,
        **kwargs,
    }
    if override_conference:
        variables["conference"] = override_conference

    return (
        client.query(
            """mutation($input: SendSubmissionInput!) {
                sendSubmission(input: $input) {
                    __typename

                    ... on Submission {
                        id
                        title(language: "en")
                        abstract(language: "en")
                        elevatorPitch(language: "en")
                        shortSocialSummary
                        audienceLevel {
                            name
                        }
                        languages {
                            code
                            name
                        }
                        notes
                        tags {
                            name
                        }
                        doNotRecord
                    }

                    ... on SendSubmissionErrors {
                        errors {
                            validationConference: conference
                            validationTopic: topic
                            validationTitle: title
                            validationAbstract: abstract
                            validationLanguages: languages
                            validationNotes: notes
                            validationType: type
                            validationDuration: duration
                            validationAudienceLevel: audienceLevel
                            validationTags: tags
                            validationPreviousTalkVideo: previousTalkVideo
                            validationPreviousSpeakerLevel: speakerLevel
                            validationShortSocialSummary: shortSocialSummary
                            validationSpeakerBio: speakerBio
                            validationSpeakerPhoto: speakerPhoto
                            validationSpeakerWebsite: speakerWebsite
                            validationSpeakerTwitterHandle: speakerTwitterHandle
                            validationSpeakerInstagramHandle: speakerInstagramHandle
                            validationSpeakerLinkedinUrl: speakerLinkedinUrl
                            validationSpeakerFacebookUrl: speakerFacebookUrl
                            validationSpeakerMastodonHandle: speakerMastodonHandle
                            nonFieldErrors
                        }
                    }
                }
            }""",
            variables={"input": variables},
        ),
        variables,
    )


def test_submit_talk(
    graphql_client,
    user,
    django_capture_on_commit_callbacks,
    mocker,
    settings,
    sent_emails,
):
    settings.FRONTEND_URL = "http://testserver"
    mock_notify = mocker.patch("api.submissions.mutations.notify_new_cfp_submission")
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("my-topic",),
        languages=("en",),
        submission_types=("talk",),
        active_cfp=True,
        durations=("50",),
        audience_levels=("Beginner",),
    )

    EmailTemplateFactory(
        conference=conference,
        identifier=EmailTemplateIdentifier.proposal_received_confirmation,
    )

    speaker_photo = FileFactory().id

    with django_capture_on_commit_callbacks(execute=True):
        resp, variables = _submit_talk(
            graphql_client,
            conference,
            title={
                "en": "English",
                "it": "old old",
            },
            shortSocialSummary="summary",
            speakerBio="my bio",
            speakerPhoto=speaker_photo,
            speakerAvailabilities={
                "2023-10-10@am": "preferred",
                "2023-10-11@pm": "unavailable",
                "2023-10-12@am": "available",
            },
        )

    assert resp["data"]["sendSubmission"]["__typename"] == "Submission"

    assert resp["data"]["sendSubmission"]["title"] == "English"
    assert resp["data"]["sendSubmission"]["abstract"] == variables["abstract"]["en"]
    assert resp["data"]["sendSubmission"]["shortSocialSummary"] == "summary"

    talk = Submission.objects.get_by_hashid(resp["data"]["sendSubmission"]["id"])

    assert talk.title.localize("en") == "English"
    assert talk.abstract.localize("en") == variables["abstract"]["en"]

    assert talk.title.data.get("it") is None
    assert talk.abstract.data.get("it") is None

    assert len(talk.languages.all()) == 1
    assert len(talk.languages.filter(code="en")) == 1
    assert talk.topic.name == "my-topic"
    assert talk.conference == conference
    assert talk.speaker_id == user.id
    assert talk.audience_level.name == "Beginner"
    assert talk.short_social_summary == "summary"
    assert talk.do_not_record is False

    participant = Participant.objects.get(conference=conference, user_id=user.id)
    assert participant.bio == "my bio"
    assert participant.photo_file_id == speaker_photo
    assert participant.speaker_availabilities == {
        "2023-10-10@am": "preferred",
        "2023-10-11@pm": "unavailable",
        "2023-10-12@am": "available",
    }

    assert PrivacyPolicyAcceptanceRecord.objects.filter(
        user=user, conference=conference, privacy_policy="cfp"
    ).exists()

    mock_notify.delay.assert_called_once()

    # Verify that the correct email template was used and email was sent
    emails_sent = sent_emails()
    assert emails_sent.count() == 1

    sent_email = emails_sent.first()
    assert (
        sent_email.email_template.identifier
        == EmailTemplateIdentifier.proposal_received_confirmation
    )
    assert sent_email.email_template.conference == conference
    assert sent_email.recipient == user
    assert sent_email.recipient_email == user.email

    # Verify placeholders were processed correctly
    assert sent_email.placeholders["user_name"] == user.full_name
    assert sent_email.placeholders["proposal_title"] == "English"
    assert (
        sent_email.placeholders["proposal_url"]
        == f"http://testserver/submission/{talk.hashid}"
    )


def test_submit_talk_with_photo_to_upload(graphql_client, user, mocker):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("my-topic",),
        languages=("en",),
        submission_types=("talk",),
        active_cfp=True,
        durations=("50",),
        audience_levels=("Beginner",),
    )
    EmailTemplateFactory(
        conference=conference,
        identifier=EmailTemplateIdentifier.proposal_received_confirmation,
    )
    speaker_photo = FileFactory().id

    resp, variables = _submit_talk(
        graphql_client,
        conference,
        title={
            "en": "English",
            "it": "old old",
        },
        shortSocialSummary="summary",
        speakerBio="my bio",
        speakerPhoto=speaker_photo,
    )

    assert resp["data"]["sendSubmission"]["__typename"] == "Submission"

    participant = Participant.objects.get(conference=conference, user_id=user.id)
    assert participant.photo_file_id == speaker_photo


def test_submit_talk_without_photo_fails(graphql_client, user, mocker):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("my-topic",),
        languages=("en",),
        submission_types=("talk",),
        active_cfp=True,
        durations=("50",),
        audience_levels=("Beginner",),
    )

    EmailTemplateFactory(
        conference=conference,
        identifier=EmailTemplateIdentifier.proposal_received_confirmation,
    )

    resp, variables = _submit_talk(
        graphql_client,
        conference,
        title={
            "en": "English",
            "it": "old old",
        },
        shortSocialSummary="summary",
        speakerBio="my bio",
        speakerPhoto="",
    )

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    assert resp["data"]["sendSubmission"]["errors"]["validationSpeakerPhoto"] == [
        "This is required"
    ]


def test_submit_talk_with_existing_participant(graphql_client, user):
    graphql_client.force_login(user)
    conference = ConferenceFactory(
        topics=("my-topic",),
        languages=("en",),
        submission_types=("talk",),
        active_cfp=True,
        durations=("50",),
        audience_levels=("Beginner",),
    )

    EmailTemplateFactory(
        conference=conference,
        identifier=EmailTemplateIdentifier.proposal_received_confirmation,
    )

    participant = Participant.objects.create(
        conference=conference, user_id=user.id, bio="old bio"
    )

    speaker_photo = FileFactory().id

    resp, variables = _submit_talk(
        graphql_client,
        conference,
        title={
            "en": "English",
            "it": "old old",
        },
        shortSocialSummary="summary",
        speakerBio="my bio",
        speakerPhoto=speaker_photo,
    )

    assert resp["data"]["sendSubmission"]["__typename"] == "Submission"

    assert resp["data"]["sendSubmission"]["title"] == "English"
    assert resp["data"]["sendSubmission"]["abstract"] == variables["abstract"]["en"]
    assert resp["data"]["sendSubmission"]["shortSocialSummary"] == "summary"

    talk = Submission.objects.get_by_hashid(resp["data"]["sendSubmission"]["id"])

    assert talk.title.localize("en") == "English"
    assert talk.abstract.localize("en") == variables["abstract"]["en"]

    assert talk.title.data.get("it") is None
    assert talk.abstract.data.get("it") is None

    assert len(talk.languages.all()) == 1
    assert len(talk.languages.filter(code="en")) == 1
    assert talk.topic.name == "my-topic"
    assert talk.conference == conference
    assert talk.speaker_id == user.id
    assert talk.audience_level.name == "Beginner"
    assert talk.short_social_summary == "summary"

    participant.refresh_from_db()
    assert participant.bio == "my bio"
    assert participant.photo_file_id == speaker_photo


def test_submit_talk_with_missing_data_of_other_language_fails(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("my-topic",),
        languages=("en", "it"),
        submission_types=("talk",),
        active_cfp=True,
        durations=("50",),
        audience_levels=("Beginner",),
    )

    EmailTemplateFactory(
        conference=conference,
        identifier=EmailTemplateIdentifier.proposal_received_confirmation,
    )

    resp, _ = _submit_talk(
        graphql_client,
        conference,
        title={
            "en": "English",
            "it": "",
        },
        abstract={"en": "abstract", "it": ""},
    )

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    assert resp["data"]["sendSubmission"]["errors"]["validationAbstract"] == [
        "Italian: Cannot be empty"
    ]
    assert resp["data"]["sendSubmission"]["errors"]["validationTitle"] == [
        "Italian: Cannot be empty"
    ]


def test_submit_talk_with_missing_data_fails(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("my-topic",),
        languages=("en", "it"),
        submission_types=("talk",),
        active_cfp=True,
        durations=("50",),
        audience_levels=("Beginner",),
    )

    EmailTemplateFactory(
        conference=conference,
        identifier=EmailTemplateIdentifier.proposal_received_confirmation,
    )

    resp, _ = _submit_talk(
        graphql_client,
        conference,
        title={
            "en": "",
            "it": "",
        },
        abstract={"en": "", "it": ""},
    )

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"

    assert (
        "Italian: Cannot be empty"
        in resp["data"]["sendSubmission"]["errors"]["validationAbstract"]
    )
    assert (
        "English: Cannot be empty"
        in resp["data"]["sendSubmission"]["errors"]["validationAbstract"]
    )

    assert (
        "Italian: Cannot be empty"
        in resp["data"]["sendSubmission"]["errors"]["validationTitle"]
    )
    assert (
        "English: Cannot be empty"
        in resp["data"]["sendSubmission"]["errors"]["validationTitle"]
    )


def test_submit_talk_with_multiple_languages(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("my-topic",),
        languages=("it", "en"),
        submission_types=("talk",),
        active_cfp=True,
        durations=("50",),
        audience_levels=("Beginner",),
    )

    EmailTemplateFactory(
        conference=conference,
        identifier=EmailTemplateIdentifier.proposal_received_confirmation,
    )

    resp, variables = _submit_talk(
        graphql_client,
        conference,
        title={
            "en": "English",
            "it": "Italian",
        },
    )

    assert resp["data"]["sendSubmission"]["__typename"] == "Submission"

    assert resp["data"]["sendSubmission"]["title"] == "English"
    assert resp["data"]["sendSubmission"]["abstract"] == variables["abstract"]["en"]

    talk = Submission.objects.get_by_hashid(resp["data"]["sendSubmission"]["id"])

    assert talk.title.localize("en") == "English"
    assert talk.abstract.localize("en") == variables["abstract"]["en"]

    assert talk.title.localize("it") == "Italian"
    assert talk.abstract.localize("it") == variables["abstract"]["it"]

    assert len(talk.languages.all()) == 2
    assert len(talk.languages.filter(code="it")) == 1
    assert len(talk.languages.filter(code="en")) == 1
    assert talk.topic.name == "my-topic"
    assert talk.conference == conference
    assert talk.speaker_id == user.id
    assert talk.audience_level.name == "Beginner"


def test_submit_talk_with_not_valid_conf_language(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("my-topic",),
        languages=("it",),
        submission_types=("talk",),
        durations=("50",),
        active_cfp=True,
        audience_levels=("Beginner",),
    )

    resp, _ = _submit_talk(graphql_client, conference, languages=["en"])

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    assert resp["data"]["sendSubmission"]["errors"]["validationLanguages"] == [
        "Language (en) is not allowed"
    ]


def test_submit_talk_with_not_valid_duration(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("my-topic",),
        languages=("it",),
        submission_types=("talk",),
        durations=("50",),
        active_cfp=True,
        audience_levels=("Beginner",),
    )

    resp, _ = _submit_talk(graphql_client, conference, duration=8)

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    assert resp["data"]["sendSubmission"]["errors"]["validationDuration"] == [
        "Select a valid choice. That choice is not one of the available choices."
    ]


def test_cannot_use_duration_if_submission_type_is_not_allowed(graphql_client, user):
    graphql_client.force_login(user)

    talk_type = SubmissionTypeFactory(name="talk")
    tutorial_type = SubmissionTypeFactory(name="tutorial")

    conference = ConferenceFactory(
        topics=("my-topic",),
        languages=("it",),
        submission_types=("talk", "tutorial"),
        active_cfp=True,
        audience_levels=("Beginner",),
    )

    duration1 = DurationFactory(conference=conference)
    duration1.allowed_submission_types.add(talk_type)

    duration2 = DurationFactory(conference=conference)
    duration2.allowed_submission_types.add(tutorial_type)

    resp, _ = _submit_talk(
        graphql_client, conference, type=talk_type.id, duration=duration2.id
    )

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    assert resp["data"]["sendSubmission"]["errors"]["validationDuration"] == [
        "Duration is not an allowed for the submission type"
    ]


def test_submit_talk_with_duration_id_of_another_conf(graphql_client, user):
    graphql_client.force_login(user)

    another_conf_duration = DurationFactory()

    conference = ConferenceFactory(
        topics=("my-topic",),
        languages=("it",),
        submission_types=("talk",),
        durations=("50",),
        active_cfp=True,
        audience_levels=("Beginner",),
    )

    resp, _ = _submit_talk(
        graphql_client, conference, duration=another_conf_duration.id
    )

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    assert resp["data"]["sendSubmission"]["errors"]["validationDuration"] == [
        "Select a valid choice. That choice is not one of the available choices."
    ]


def test_submit_talk_with_not_valid_conf_topic(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("my-topic",),
        languages=("it",),
        submission_types=("talk",),
        active_cfp=True,
        durations=("50",),
        audience_levels=("Beginner",),
    )
    topic = TopicFactory(name="random topic")

    resp, _ = _submit_talk(graphql_client, conference, topic=topic.id)

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    assert resp["data"]["sendSubmission"]["errors"]["validationTopic"] == [
        "Not a valid topic"
    ]


def test_submit_talk_with_not_valid_allowed_submission_type_in_the_conference(
    graphql_client, user
):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("my-topic",),
        languages=("it",),
        submission_types=("tutorial",),
        active_cfp=True,
        durations=("50",),
        audience_levels=("Beginner",),
    )

    resp, _ = _submit_talk(graphql_client, conference)

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    assert resp["data"]["sendSubmission"]["errors"]["validationType"] == [
        "Not allowed submission type"
    ]


def test_submit_talk_with_not_valid_submission_type_id(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("my-topic",),
        languages=("it",),
        submission_types=("tutorial",),
        active_cfp=True,
        durations=("50",),
        audience_levels=("Beginner",),
    )

    resp, _ = _submit_talk(graphql_client, conference, type=999)

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    assert resp["data"]["sendSubmission"]["errors"]["validationType"] == [
        "Not allowed submission type"
    ]


def test_submit_talk_with_not_valid_language_code(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("my-topic",),
        languages=("it",),
        submission_types=("tutorial",),
        active_cfp=True,
        durations=("50",),
        audience_levels=("Beginner",),
    )

    resp, _ = _submit_talk(graphql_client, conference, languages=["fit"])

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    assert resp["data"]["sendSubmission"]["errors"]["validationLanguages"] == [
        "Language (fit) is not allowed"
    ]


def test_submit_talk_with_not_valid_audience_level(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("my-topic",),
        languages=("it",),
        submission_types=("talk",),
        durations=("50",),
        active_cfp=True,
        audience_levels=("Beginner",),
    )
    resp, _ = _submit_talk(graphql_client, conference, audienceLevel=50)

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    # assert resp["data"]["sendSubmission"]["submission"] is None
    assert resp["data"]["sendSubmission"]["errors"]["validationAudienceLevel"] == [
        "Not a valid audience level"
    ]
    # assert resp["data"]["sendSubmission"]["errors"][0]["field"] == "audience_level"


def test_submit_talk_with_not_valid_conf_audience_level(graphql_client, user):
    graphql_client.force_login(user)
    audience_level = AudienceLevelFactory(name="Intermidiate")

    conference = ConferenceFactory(
        topics=("my-topic",),
        languages=("it",),
        submission_types=("talk",),
        durations=("50",),
        active_cfp=True,
        audience_levels=("Beginner",),
    )
    resp, _ = _submit_talk(graphql_client, conference, audienceLevel=audience_level.id)

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    assert resp["data"]["sendSubmission"]["errors"]["validationAudienceLevel"] == [
        "Not a valid audience level"
    ]


def test_cannot_propose_a_talk_as_unlogged_user(graphql_client):
    conference = ConferenceFactory(
        topics=("my-topic",),
        languages=("it",),
        submission_types=("talk",),
        durations=("50",),
        audience_levels=("Beginner",),
    )

    resp, _ = _submit_talk(graphql_client, conference)

    assert resp["errors"][0]["message"] == "User not logged in"


def test_cannot_propose_a_talk_if_the_cfp_is_not_open(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("friends",),
        languages=("it",),
        active_cfp=False,
        submission_types=("talk",),
        durations=("50",),
        audience_levels=("Beginner",),
    )

    resp, _ = _submit_talk(graphql_client, conference)

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    assert resp["data"]["sendSubmission"]["errors"]["nonFieldErrors"] == [
        "The call for paper is not open!"
    ]


def test_cannot_propose_a_talk_if_a_cfp_is_not_specified(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("friends",),
        languages=("it",),
        submission_types=("talk",),
        durations=("50",),
        audience_levels=("Beginner",),
    )

    EmailTemplateFactory(
        conference=conference,
        identifier=EmailTemplateIdentifier.proposal_received_confirmation,
    )

    resp, _ = _submit_talk(graphql_client, conference)

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    assert resp["data"]["sendSubmission"]["errors"]["nonFieldErrors"] == [
        "The call for paper is not open!"
    ]


def test_same_user_can_propose_multiple_talks_to_the_same_conference(
    graphql_client, user
):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("friends",),
        languages=("en",),
        active_cfp=True,
        submission_types=("talk",),
        durations=("50",),
        audience_levels=("Beginner",),
    )

    EmailTemplateFactory(
        conference=conference,
        identifier=EmailTemplateIdentifier.proposal_received_confirmation,
    )

    resp, _ = _submit_talk(graphql_client, conference, title={"en": "My first talk"})

    assert resp["data"]["sendSubmission"]["title"] == "My first talk"

    assert (
        Submission.objects.filter(speaker_id=user.id, conference=conference).count()
        == 1
    )

    resp, _ = _submit_talk(graphql_client, conference, title={"en": "Another talk"})

    assert resp["data"]["sendSubmission"]["title"] == "Another talk"

    assert (
        Submission.objects.filter(speaker_id=user.id, conference=conference).count()
        == 2
    )


def test_submit_tutorial(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("friends",),
        languages=("en",),
        active_cfp=True,
        submission_types=("talk", "tutorial"),
        durations=("50",),
        audience_levels=("Beginner",),
    )

    EmailTemplateFactory(
        conference=conference,
        identifier=EmailTemplateIdentifier.proposal_received_confirmation,
    )

    resp, _ = _submit_tutorial(
        graphql_client, conference, title={"en": "My first tutorial"}
    )

    assert resp["data"]["sendSubmission"]["__typename"] == "Submission"
    assert resp["data"]["sendSubmission"]["title"] == "My first tutorial"

    assert (
        Submission.objects.filter(speaker_id=user.id, conference=conference).count()
        == 1
    )


def test_submit_tutorial_and_talk_to_the_same_conference(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("friends",),
        languages=("en",),
        active_cfp=True,
        submission_types=("talk", "tutorial"),
        durations=("50",),
        audience_levels=("Beginner",),
    )

    EmailTemplateFactory(
        conference=conference,
        identifier=EmailTemplateIdentifier.proposal_received_confirmation,
    )

    resp, _ = _submit_tutorial(
        graphql_client, conference, title={"en": "My first tutorial"}
    )

    assert resp["data"]["sendSubmission"]["title"] == "My first tutorial"

    assert (
        Submission.objects.filter(speaker_id=user.id, conference=conference).count()
        == 1
    )

    resp, _ = _submit_talk(graphql_client, conference, title={"en": "My first talk"})

    assert resp["data"]["sendSubmission"]["title"] == "My first talk"

    assert (
        Submission.objects.filter(speaker_id=user.id, conference=conference).count()
        == 2
    )


def test_notes_are_not_required(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("friends",),
        languages=("en",),
        active_cfp=True,
        submission_types=("talk", "tutorial"),
        durations=("50",),
        audience_levels=("Beginner",),
    )

    EmailTemplateFactory(
        conference=conference,
        identifier=EmailTemplateIdentifier.proposal_received_confirmation,
    )

    resp, _ = _submit_tutorial(graphql_client, conference, notes="")

    assert resp["data"]["sendSubmission"]["__typename"] == "Submission"
    assert resp["data"]["sendSubmission"]["notes"] == ""

    assert (
        Submission.objects.filter(speaker_id=user.id, conference=conference).count()
        == 1
    )


def test_same_user_can_submit_talks_to_different_conferences(graphql_client, user):
    graphql_client.force_login(user)

    conference1 = ConferenceFactory(
        topics=("friends",),
        languages=("en",),
        active_cfp=True,
        submission_types=("talk",),
        durations=("50",),
        audience_levels=("Beginner",),
    )

    conference2 = ConferenceFactory(
        topics=("another-stuff",),
        languages=("en",),
        active_cfp=True,
        submission_types=("talk",),
        durations=("50",),
        audience_levels=("Beginner",),
    )

    EmailTemplateFactory(
        conference=conference1,
        identifier=EmailTemplateIdentifier.proposal_received_confirmation,
    )

    EmailTemplateFactory(
        conference=conference2,
        identifier=EmailTemplateIdentifier.proposal_received_confirmation,
    )

    resp, _ = _submit_talk(graphql_client, conference1, title={"en": "My first talk"})

    assert resp["data"]["sendSubmission"]["title"] == "My first talk"

    assert (
        Submission.objects.filter(speaker_id=user.id, conference=conference1).count()
        == 1
    )
    assert (
        Submission.objects.filter(speaker_id=user.id, conference=conference2).count()
        == 0
    )

    resp, _ = _submit_talk(graphql_client, conference2, title={"en": "Another talk"})

    assert resp["data"]["sendSubmission"]["title"] == "Another talk"

    assert (
        Submission.objects.filter(speaker_id=user.id, conference=conference1).count()
        == 1
    )
    assert (
        Submission.objects.filter(speaker_id=user.id, conference=conference2).count()
        == 1
    )


def test_create_submission_tags(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("friends",),
        languages=("it",),
        active_cfp=True,
        submission_types=("talk", "tutorial"),
        durations=("50",),
        audience_levels=("Beginner",),
    )

    EmailTemplateFactory(
        conference=conference,
        identifier=EmailTemplateIdentifier.proposal_received_confirmation,
    )

    python, _ = SubmissionTag.objects.get_or_create(name="python")
    graphql, _ = SubmissionTag.objects.get_or_create(name="GraphQL")

    resp, variables = _submit_talk(
        graphql_client, conference, tags=[python.id, graphql.id]
    )

    assert resp["data"]["sendSubmission"]["__typename"] == "Submission"
    assert resp["data"]["sendSubmission"]["tags"] == [
        {"name": "python"},
        {"name": "GraphQL"},
    ]


def test_speaker_level_is_required(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("friends",),
        languages=("it",),
        active_cfp=True,
        submission_types=("talk", "tutorial"),
        durations=("50",),
        audience_levels=("Beginner",),
    )

    resp, _ = _submit_tutorial(graphql_client, conference, speakerLevel="")
    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    assert resp["data"]["sendSubmission"]["errors"][
        "validationPreviousSpeakerLevel"
    ] == ["You need to specify what is your speaker experience"]


def test_speaker_level_only_allows_the_predefined_levels(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("friends",),
        languages=("it",),
        active_cfp=True,
        submission_types=("talk", "tutorial"),
        durations=("50",),
        audience_levels=("Beginner",),
    )

    resp, _ = _submit_tutorial(graphql_client, conference, speakerLevel="just_started")
    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    assert resp["data"]["sendSubmission"]["errors"][
        "validationPreviousSpeakerLevel"
    ] == ["Select a valid choice"]


def test_submit_talk_with_too_long_title_fails(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("my-topic",),
        languages=("en", "it"),
        submission_types=("talk",),
        active_cfp=True,
        durations=("50",),
        audience_levels=("Beginner",),
    )

    resp, _ = _submit_talk(
        graphql_client,
        conference,
        title={
            "en": "very long title" * 50,
            "it": "",
        },
    )

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"

    assert (
        "Italian: Cannot be empty"
        in resp["data"]["sendSubmission"]["errors"]["validationTitle"]
    )
    assert (
        "English: Cannot be more than 100 chars"
        in resp["data"]["sendSubmission"]["errors"]["validationTitle"]
    )


def test_submit_talk_with_no_languages_and_no_tags_is_not_allowed(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("my-topic",),
        languages=("en", "it"),
        submission_types=("talk",),
        active_cfp=True,
        durations=("50",),
        audience_levels=("Beginner",),
    )

    resp, _ = _submit_talk(graphql_client, conference, languages=[], tags=[])

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"

    assert (
        "You need to add at least one language"
        in resp["data"]["sendSubmission"]["errors"]["validationLanguages"]
    )

    assert (
        "You need to add at least one tag"
        in resp["data"]["sendSubmission"]["errors"]["validationTags"]
    )


def test_submit_talk_with_no_conference(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("my-topic",),
        languages=("en", "it"),
        submission_types=("talk",),
        active_cfp=True,
        durations=("50",),
        audience_levels=("Beginner",),
    )

    resp, _ = _submit_talk(graphql_client, conference, override_conference="abc-abc")

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"

    assert (
        "Invalid conference"
        in resp["data"]["sendSubmission"]["errors"]["validationConference"]
    )


def test_submit_talk_with_too_long_notes_fails(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("my-topic",),
        languages=("en", "it"),
        submission_types=("talk",),
        active_cfp=True,
        durations=("50",),
        audience_levels=("Beginner",),
    )

    resp, _ = _submit_talk(
        graphql_client,
        conference,
        notes="abc" * 2000,
    )

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"

    assert (
        "Cannot be more than 1000 chars"
        in resp["data"]["sendSubmission"]["errors"]["validationNotes"]
    )


def test_submit_talk_with_too_long_summary_fails(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("my-topic",),
        languages=("en", "it"),
        submission_types=("talk",),
        active_cfp=True,
        durations=("50",),
        audience_levels=("Beginner",),
    )

    resp, _ = _submit_talk(
        graphql_client,
        conference,
        shortSocialSummary="summary" * 2000,
    )

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"

    assert (
        "Cannot be more than 128 chars"
        in resp["data"]["sendSubmission"]["errors"]["validationShortSocialSummary"]
    )


def test_submit_talk_only_allows_5_tags(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("my-topic",),
        languages=("en", "it"),
        submission_types=("talk",),
        active_cfp=True,
        durations=("50",),
        audience_levels=("Beginner",),
    )

    tag1, _ = SubmissionTag.objects.get_or_create(name="tag1")
    tag2, _ = SubmissionTag.objects.get_or_create(name="tag2")
    tag3, _ = SubmissionTag.objects.get_or_create(name="tag3")
    tag4, _ = SubmissionTag.objects.get_or_create(name="tag4")
    tag5, _ = SubmissionTag.objects.get_or_create(name="tag5")
    tag6, _ = SubmissionTag.objects.get_or_create(name="tag6")

    resp, _ = _submit_talk(
        graphql_client,
        conference,
        shortSocialSummary="summary",
        tags=[tag1.id, tag2.id, tag3.id, tag4.id, tag5.id, tag6.id],
    )

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"

    assert (
        "You can only add up to 3 tags"
        in resp["data"]["sendSubmission"]["errors"]["validationTags"]
    )


def test_submit_talk_with_no_tags_fails(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("my-topic",),
        languages=("en", "it"),
        submission_types=("talk",),
        active_cfp=True,
        durations=("50",),
        audience_levels=("Beginner",),
    )

    resp, _ = _submit_talk(
        graphql_client, conference, shortSocialSummary="summary", tags=[]
    )

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"

    assert (
        "You need to add at least one tag"
        in resp["data"]["sendSubmission"]["errors"]["validationTags"]
    )


def test_cannot_submit_more_than_3_proposals(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("my-topic",),
        languages=("en", "it"),
        submission_types=("talk",),
        active_cfp=True,
        durations=("50",),
        audience_levels=("Beginner",),
        max_proposals_per_user=3,
    )

    SubmissionFactory(
        speaker_id=user.id,
        conference=conference,
        status=Submission.STATUS.proposed,
    )
    SubmissionFactory(
        speaker_id=user.id,
        conference=conference,
        status=Submission.STATUS.proposed,
    )
    SubmissionFactory(
        speaker_id=user.id,
        conference=conference,
        status=Submission.STATUS.proposed,
    )

    resp, _ = _submit_talk(graphql_client, conference, title={"en": "My first talk"})

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    assert resp["data"]["sendSubmission"]["errors"]["nonFieldErrors"] == [
        "You can only submit up to 3 proposals"
    ]


def test_can_submit_unlimited_proposals_when_max_proposals_is_none(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("my-topic",),
        languages=("en", "it"),
        submission_types=("talk",),
        active_cfp=True,
        durations=("50",),
        audience_levels=("Beginner",),
        # max_proposals_per_user defaults to None (no limit)
    )

    EmailTemplateFactory(
        conference=conference,
        identifier=EmailTemplateIdentifier.proposal_received_confirmation,
    )

    # Create 3 existing submissions
    for _ in range(3):
        SubmissionFactory(
            speaker_id=user.id,
            conference=conference,
            status=Submission.STATUS.proposed,
        )

    # Should be able to submit a 4th proposal
    resp, _ = _submit_talk(graphql_client, conference, title={"en": "My fourth talk"})

    assert resp["data"]["sendSubmission"]["__typename"] == "Submission"
    assert resp["data"]["sendSubmission"]["title"] == "My fourth talk"


def test_submit_talk_with_do_not_record_true(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory(
        topics=("my-topic",),
        languages=("en", "it"),
        submission_types=("talk",),
        active_cfp=True,
        durations=("50",),
        audience_levels=("Beginner",),
    )

    EmailTemplateFactory(
        conference=conference,
        identifier=EmailTemplateIdentifier.proposal_received_confirmation,
    )

    resp, _ = _submit_talk(graphql_client, conference, doNotRecord=True)

    assert resp["data"]["sendSubmission"]["__typename"] == "Submission"
    assert resp["data"]["sendSubmission"]["doNotRecord"] is True

    talk = Submission.objects.get_by_hashid(resp["data"]["sendSubmission"]["id"])
    assert talk.do_not_record is True
