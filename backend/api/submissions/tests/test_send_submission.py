from pytest import mark

from submissions.models import Submission, SubmissionTag, SubmissionType
from submissions.tests.factories import SubmissionFactory


def _submit_talk(client, conference, **kwargs):
    tag, _ = SubmissionTag.objects.get_or_create(name="tag")

    talk = SubmissionFactory.build(
        type=SubmissionType.objects.get_or_create(name="talk")[0]
    )

    languages = [language.code for language in conference.languages.all()]

    defaults = {
        "title": {
            "en": talk.title.data.get("en", ""),
            "it": talk.title.data.get("it", ""),
        },
        "abstract": {
            "en": talk.abstract.data.get("en", ""),
            "it": talk.abstract.data.get("it", ""),
        },
        "elevator_pitch": {
            "en": talk.elevator_pitch.data.get("en", ""),
            "it": talk.elevator_pitch.data.get("it", ""),
        },
        "notes": talk.notes,
        "languages": languages,
        "conference": conference.code,
        "topic": conference.topics.first().id,
        "type": talk.type.id,
        "duration": conference.durations.first().id,
        "audience_level": conference.audience_levels.first().id,
        "speaker_level": talk.speaker_level,
        "previous_talk_video": talk.previous_talk_video,
        "tags": [tag.id],
    }

    variables = {**defaults, **kwargs}
    return (
        client.query(
            """mutation(
                $conference: ID!,
                $topic: ID!,
                $title: MultiLingualInput!,
                $elevator_pitch: MultiLingualInput!,
                $abstract: MultiLingualInput!,
                $notes: String!,
                $languages: [ID!]!,
                $type: ID!,
                $duration: ID!,
                $audience_level: ID!,
                $tags: [ID!],
                $speaker_level: String!
                $previous_talk_video: String!
            ) {
                sendSubmission(input: {
                    title: $title,
                    abstract: $abstract,
                    languages: $languages,
                    conference: $conference,
                    elevatorPitch: $elevator_pitch,
                    notes: $notes,
                    topic: $topic,
                    type: $type,
                    duration: $duration,,
                    audienceLevel: $audience_level
                    tags: $tags
                    speakerLevel: $speaker_level
                    previousTalkVideo: $previous_talk_video
                }) {
                    __typename

                    ... on Submission {
                        id
                        title(language: "en")
                        abstract(language: "en")
                        elevatorPitch(language: "en")
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
                    }

                    ... on SendSubmissionErrors {
                        validationConference: conference
                        validationTopic: topic
                        validationTitle: title
                        validationAbstract: abstract
                        validationLanguages: languages
                        validationType: type
                        validationDuration: duration
                        validationAudienceLevel: audienceLevel
                        validationTags: tags
                        validationPreviousTalkVideo: previousTalkVideo
                        validationPreviousSpeakerLevel: speakerLevel
                        nonFieldErrors
                    }
                }
            }""",
            variables=variables,
        ),
        variables,
    )


def _submit_tutorial(client, conference, **kwargs):
    tag, _ = SubmissionTag.objects.get_or_create(name="tag")

    talk = SubmissionFactory.create(
        type=SubmissionType.objects.get_or_create(name="tutorial")[0]
    )
    talk.tags.add(tag)

    languages = [language.code for language in conference.languages.all()]

    defaults = {
        "title": {
            "en": talk.title.data.get("en", ""),
            "it": talk.title.data.get("it", ""),
        },
        "abstract": {
            "en": talk.abstract.data.get("en", ""),
            "it": talk.abstract.data.get("it", ""),
        },
        "elevator_pitch": {
            "en": talk.elevator_pitch.data.get("en", ""),
            "it": talk.elevator_pitch.data.get("it", ""),
        },
        "notes": talk.notes,
        "languages": languages,
        "conference": conference.code,
        "topic": conference.topics.first().id,
        "type": talk.type.id,
        "duration": conference.durations.first().id,
        "audience_level": conference.audience_levels.first().id,
        "tags": [tag.id for tag in talk.tags.all()],
        "speaker_level": talk.speaker_level,
        "previous_talk_video": talk.previous_talk_video,
    }

    variables = {**defaults, **kwargs}

    return (
        client.query(
            """mutation(
                $conference: ID!,
                $topic: ID!,
                $title: MultiLingualInput!,
                $elevator_pitch: MultiLingualInput!,
                $abstract: MultiLingualInput!,
                $notes: String!,
                $languages: [ID!]!,
                $type: ID!,
                $duration: ID!,
                $audience_level: ID!,
                $tags: [ID!],
                $speaker_level: String!
                $previous_talk_video: String!
            ) {
                sendSubmission(input: {
                    title: $title,
                    abstract: $abstract,
                    languages: $languages,
                    conference: $conference,
                    topic: $topic,
                    type: $type,
                    duration: $duration,
                    audienceLevel: $audience_level,
                    tags: $tags,
                    notes: $notes,
                    elevatorPitch: $elevator_pitch,
                    speakerLevel: $speaker_level,
                    previousTalkVideo: $previous_talk_video
                }) {
                    __typename

                    ... on Submission {
                        id
                        title(language: "en")
                        abstract(language: "en")
                        elevatorPitch(language: "en")
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
                    }

                    ... on SendSubmissionErrors {
                        validationConference: conference
                        validationTopic: topic
                        validationTitle: title
                        validationAbstract: abstract
                        validationLanguages: languages
                        validationType: type
                        validationDuration: duration
                        validationAudienceLevel: audienceLevel
                        validationTags: tags
                        validationPreviousTalkVideo: previousTalkVideo
                        validationPreviousSpeakerLevel: speakerLevel
                        nonFieldErrors
                    }
                }
            }""",
            variables=variables,
        ),
        variables,
    )


@mark.django_db
def test_submit_talk(graphql_client, user, conference_factory):
    graphql_client.force_login(user)

    conference = conference_factory(
        topics=("my-topic",),
        languages=("en",),
        submission_types=("talk",),
        active_cfp=True,
        durations=("50",),
        audience_levels=("Beginner",),
    )

    resp, variables = _submit_talk(
        graphql_client,
        conference,
        title={
            "en": "English",
            "it": "old old",
        },
    )

    assert resp["data"]["sendSubmission"]["__typename"] == "Submission"

    assert resp["data"]["sendSubmission"]["title"] == "English"
    assert resp["data"]["sendSubmission"]["abstract"] == variables["abstract"]["en"]

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


@mark.django_db
def test_submit_talk_with_missing_data_of_other_language_fails(
    graphql_client, user, conference_factory
):
    graphql_client.force_login(user)

    conference = conference_factory(
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
            "en": "English",
            "it": "",
        },
        abstract={"en": "abstract", "it": ""},
    )

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    assert resp["data"]["sendSubmission"]["validationAbstract"] == [
        "Italian: Cannot be empty"
    ]
    assert resp["data"]["sendSubmission"]["validationTitle"] == [
        "Italian: Cannot be empty"
    ]


@mark.django_db
def test_submit_talk_with_missing_data_fails(graphql_client, user, conference_factory):
    graphql_client.force_login(user)

    conference = conference_factory(
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
            "en": "",
            "it": "",
        },
        abstract={"en": "", "it": ""},
    )

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"

    assert (
        "Italian: Cannot be empty"
        in resp["data"]["sendSubmission"]["validationAbstract"]
    )
    assert (
        "English: Cannot be empty"
        in resp["data"]["sendSubmission"]["validationAbstract"]
    )

    assert (
        "Italian: Cannot be empty" in resp["data"]["sendSubmission"]["validationTitle"]
    )
    assert (
        "English: Cannot be empty" in resp["data"]["sendSubmission"]["validationTitle"]
    )


@mark.django_db
def test_submit_talk_with_multiple_languages(graphql_client, user, conference_factory):
    graphql_client.force_login(user)

    conference = conference_factory(
        topics=("my-topic",),
        languages=("it", "en"),
        submission_types=("talk",),
        active_cfp=True,
        durations=("50",),
        audience_levels=("Beginner",),
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


@mark.django_db
def test_submit_talk_with_not_valid_conf_language(
    graphql_client, user, conference_factory
):
    graphql_client.force_login(user)

    conference = conference_factory(
        topics=("my-topic",),
        languages=("it",),
        submission_types=("talk",),
        durations=("50",),
        active_cfp=True,
        audience_levels=("Beginner",),
    )

    resp, _ = _submit_talk(graphql_client, conference, languages=["en"])

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    assert resp["data"]["sendSubmission"]["validationLanguages"] == [
        "Language (en) is not allowed"
    ]


@mark.django_db
def test_submit_talk_with_not_valid_duration(graphql_client, user, conference_factory):
    graphql_client.force_login(user)

    conference = conference_factory(
        topics=("my-topic",),
        languages=("it",),
        submission_types=("talk",),
        durations=("50",),
        active_cfp=True,
        audience_levels=("Beginner",),
    )

    resp, _ = _submit_talk(graphql_client, conference, duration=8)

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    assert resp["data"]["sendSubmission"]["validationDuration"] == [
        "Select a valid choice. That choice is not one of the available choices."
    ]


@mark.django_db
def test_cannot_use_duration_if_submission_type_is_not_allowed(
    graphql_client, user, conference_factory, duration_factory, submission_type_factory
):
    graphql_client.force_login(user)

    talk_type = submission_type_factory(name="talk")
    tutorial_type = submission_type_factory(name="tutorial")

    conference = conference_factory(
        topics=("my-topic",),
        languages=("it",),
        submission_types=("talk", "tutorial"),
        active_cfp=True,
        audience_levels=("Beginner",),
    )

    duration1 = duration_factory(conference=conference)
    duration1.allowed_submission_types.add(talk_type)

    duration2 = duration_factory(conference=conference)
    duration2.allowed_submission_types.add(tutorial_type)

    resp, _ = _submit_talk(
        graphql_client, conference, type=talk_type.id, duration=duration2.id
    )

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    assert resp["data"]["sendSubmission"]["validationDuration"] == [
        "Duration is not an allowed for the submission type"
    ]


@mark.django_db
def test_submit_talk_with_duration_id_of_another_conf(
    graphql_client, user, conference_factory, duration_factory
):
    graphql_client.force_login(user)

    another_conf_duration = duration_factory()

    conference = conference_factory(
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
    assert resp["data"]["sendSubmission"]["validationDuration"] == [
        "Select a valid choice. That choice is not one of the available choices."
    ]


@mark.django_db
def test_submit_talk_with_not_valid_conf_topic(
    graphql_client, user, conference_factory, topic_factory
):
    graphql_client.force_login(user)

    conference = conference_factory(
        topics=("my-topic",),
        languages=("it",),
        submission_types=("talk",),
        active_cfp=True,
        durations=("50",),
        audience_levels=("Beginner",),
    )
    topic = topic_factory(name="random topic")

    resp, _ = _submit_talk(graphql_client, conference, topic=topic.id)

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    assert resp["data"]["sendSubmission"]["validationTopic"] == ["Not a valid topic"]


@mark.django_db
def test_submit_talk_with_not_valid_allowed_submission_type_in_the_conference(
    graphql_client, user, conference_factory, topic_factory
):
    graphql_client.force_login(user)

    conference = conference_factory(
        topics=("my-topic",),
        languages=("it",),
        submission_types=("tutorial",),
        active_cfp=True,
        durations=("50",),
        audience_levels=("Beginner",),
    )

    resp, _ = _submit_talk(graphql_client, conference)

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    assert resp["data"]["sendSubmission"]["validationType"] == [
        "Not allowed submission type"
    ]


@mark.django_db
def test_submit_talk_with_not_valid_submission_type_id(
    graphql_client, user, conference_factory, topic_factory
):
    graphql_client.force_login(user)

    conference = conference_factory(
        topics=("my-topic",),
        languages=("it",),
        submission_types=("tutorial",),
        active_cfp=True,
        durations=("50",),
        audience_levels=("Beginner",),
    )

    resp, _ = _submit_talk(graphql_client, conference, type=5)

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    assert resp["data"]["sendSubmission"]["validationType"] == [
        "Not allowed submission type"
    ]


@mark.django_db
def test_submit_talk_with_not_valid_language_code(
    graphql_client, user, conference_factory, topic_factory
):
    graphql_client.force_login(user)

    conference = conference_factory(
        topics=("my-topic",),
        languages=("it",),
        submission_types=("tutorial",),
        active_cfp=True,
        durations=("50",),
        audience_levels=("Beginner",),
    )

    resp, _ = _submit_talk(graphql_client, conference, languages=["fit"])

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    assert resp["data"]["sendSubmission"]["validationLanguages"] == [
        "Language (fit) is not allowed"
    ]


@mark.django_db
def test_submit_talk_with_not_valid_audience_level(
    graphql_client, user, conference_factory
):
    graphql_client.force_login(user)

    conference = conference_factory(
        topics=("my-topic",),
        languages=("it",),
        submission_types=("talk",),
        durations=("50",),
        active_cfp=True,
        audience_levels=("Beginner",),
    )
    resp, _ = _submit_talk(graphql_client, conference, audience_level=50)

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    # assert resp["data"]["sendSubmission"]["submission"] is None
    assert resp["data"]["sendSubmission"]["validationAudienceLevel"] == [
        "Not a valid audience level"
    ]
    # assert resp["data"]["sendSubmission"]["errors"][0]["field"] == "audience_level"


@mark.django_db
def test_submit_talk_with_not_valid_conf_audience_level(
    graphql_client, user, conference_factory, audience_level_factory
):
    graphql_client.force_login(user)
    audience_level = audience_level_factory(name="Intermidiate")

    conference = conference_factory(
        topics=("my-topic",),
        languages=("it",),
        submission_types=("talk",),
        durations=("50",),
        active_cfp=True,
        audience_levels=("Beginner",),
    )
    resp, _ = _submit_talk(graphql_client, conference, audience_level=audience_level.id)

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    assert resp["data"]["sendSubmission"]["validationAudienceLevel"] == [
        "Not a valid audience level"
    ]


@mark.django_db
def test_cannot_propose_a_talk_as_unlogged_user(graphql_client, conference_factory):
    conference = conference_factory(
        topics=("my-topic",),
        languages=("it",),
        submission_types=("talk",),
        durations=("50",),
        audience_levels=("Beginner",),
    )

    resp, _ = _submit_talk(graphql_client, conference)

    assert resp["errors"][0]["message"] == "User not logged in"


@mark.django_db
def test_cannot_propose_a_talk_if_the_cfp_is_not_open(
    graphql_client, user, conference_factory
):
    graphql_client.force_login(user)

    conference = conference_factory(
        topics=("friends",),
        languages=("it",),
        active_cfp=False,
        submission_types=("talk",),
        durations=("50",),
        audience_levels=("Beginner",),
    )

    resp, _ = _submit_talk(graphql_client, conference)

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    assert resp["data"]["sendSubmission"]["nonFieldErrors"] == [
        "The call for paper is not open!"
    ]


@mark.django_db
def test_cannot_propose_a_talk_if_a_cfp_is_not_specified(
    graphql_client, user, conference_factory
):
    graphql_client.force_login(user)

    conference = conference_factory(
        topics=("friends",),
        languages=("it",),
        submission_types=("talk",),
        durations=("50",),
        audience_levels=("Beginner",),
    )

    resp, _ = _submit_talk(graphql_client, conference)

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    assert resp["data"]["sendSubmission"]["nonFieldErrors"] == [
        "The call for paper is not open!"
    ]


@mark.django_db
def test_same_user_can_propose_multiple_talks_to_the_same_conference(
    graphql_client, user, conference_factory
):
    graphql_client.force_login(user)

    conference = conference_factory(
        topics=("friends",),
        languages=("en",),
        active_cfp=True,
        submission_types=("talk",),
        durations=("50",),
        audience_levels=("Beginner",),
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


@mark.django_db
def test_submit_tutorial(graphql_client, user, conference_factory):
    graphql_client.force_login(user)

    conference = conference_factory(
        topics=("friends",),
        languages=("en",),
        active_cfp=True,
        submission_types=("talk", "tutorial"),
        durations=("50",),
        audience_levels=("Beginner",),
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


@mark.django_db
def test_submit_tutorial_and_talk_to_the_same_conference(
    graphql_client, user, conference_factory
):
    graphql_client.force_login(user)

    conference = conference_factory(
        topics=("friends",),
        languages=("en",),
        active_cfp=True,
        submission_types=("talk", "tutorial"),
        durations=("50",),
        audience_levels=("Beginner",),
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


@mark.django_db
def test_notes_are_not_required(graphql_client, user, conference_factory):
    graphql_client.force_login(user)

    conference = conference_factory(
        topics=("friends",),
        languages=("en",),
        active_cfp=True,
        submission_types=("talk", "tutorial"),
        durations=("50",),
        audience_levels=("Beginner",),
    )

    resp, _ = _submit_tutorial(graphql_client, conference, notes="")

    assert resp["data"]["sendSubmission"]["__typename"] == "Submission"
    assert resp["data"]["sendSubmission"]["notes"] == ""

    assert (
        Submission.objects.filter(speaker_id=user.id, conference=conference).count()
        == 1
    )


@mark.django_db
def test_same_user_can_submit_talks_to_different_conferences(
    graphql_client, user, conference_factory
):
    graphql_client.force_login(user)

    conference1 = conference_factory(
        topics=("friends",),
        languages=("en",),
        active_cfp=True,
        submission_types=("talk",),
        durations=("50",),
        audience_levels=("Beginner",),
    )

    conference2 = conference_factory(
        topics=("another-stuff",),
        languages=("en",),
        active_cfp=True,
        submission_types=("talk",),
        durations=("50",),
        audience_levels=("Beginner",),
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


def test_create_submission_tags(
    graphql_client, user, conference_factory, submission_tag_factory
):
    graphql_client.force_login(user)

    conference = conference_factory(
        topics=("friends",),
        languages=("it",),
        active_cfp=True,
        submission_types=("talk", "tutorial"),
        durations=("50",),
        audience_levels=("Beginner",),
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


def test_speaker_level_is_required(graphql_client, user, conference_factory):
    graphql_client.force_login(user)

    conference = conference_factory(
        topics=("friends",),
        languages=("it",),
        active_cfp=True,
        submission_types=("talk", "tutorial"),
        durations=("50",),
        audience_levels=("Beginner",),
    )

    resp, _ = _submit_tutorial(graphql_client, conference, speaker_level="")
    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    assert resp["data"]["sendSubmission"]["validationPreviousSpeakerLevel"] == [
        "You need to specify what is your speaker experience"
    ]


def test_speaker_level_only_allows_the_predefined_levels(
    graphql_client, user, conference_factory
):
    graphql_client.force_login(user)

    conference = conference_factory(
        topics=("friends",),
        languages=("it",),
        active_cfp=True,
        submission_types=("talk", "tutorial"),
        durations=("50",),
        audience_levels=("Beginner",),
    )

    resp, _ = _submit_tutorial(graphql_client, conference, speaker_level="just_started")
    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"
    assert resp["data"]["sendSubmission"]["validationPreviousSpeakerLevel"] == [
        "Select a valid choice"
    ]


@mark.django_db
def test_submit_talk_with_too_long_title_fails(
    graphql_client, user, conference_factory
):
    graphql_client.force_login(user)

    conference = conference_factory(
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
            "en": "very long title very long title very long title very long title very long title very long title very long",
            "it": "",
        },
    )

    assert resp["data"]["sendSubmission"]["__typename"] == "SendSubmissionErrors"

    assert (
        "Italian: Cannot be empty" in resp["data"]["sendSubmission"]["validationTitle"]
    )
    assert (
        "English: Cannot be more than 100 chars"
        in resp["data"]["sendSubmission"]["validationTitle"]
    )


@mark.django_db
def test_submit_talk_with_no_languages_and_no_tags_is_not_allowed(
    graphql_client, user, conference_factory
):
    graphql_client.force_login(user)

    conference = conference_factory(
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
        in resp["data"]["sendSubmission"]["validationLanguages"]
    )

    assert (
        "You need to add at least one tag"
        in resp["data"]["sendSubmission"]["validationTags"]
    )
