from pytest import mark

from django.utils import timezone

from submissions.models import Submission, SubmissionType

from .factories import SubmissionFactory


def _submit_talk(client, conference, **kwargs):
    talk = SubmissionFactory.build(
        type=SubmissionType.objects.get_or_create(name='talk')[0]
    )

    defaults = {
        'title': talk.title,
        'abstract': talk.abstract,
        'elevator_pitch': talk.elevator_pitch,
        'notes': talk.notes,
        'language': 'it',
        'conference': conference.code,
        'topic': conference.topics.first().id,
        'type': talk.type.id,
        'duration': conference.durations.first().id,
    }

    variables = {**defaults, **kwargs}

    return client.query(
        """
        mutation($conference: ID!, $topic: ID!, $title: String!, $abstract: String!, $language: ID!, $type: ID!, $duration: ID!) {
            sendSubmission(input: {
                title: $title,
                abstract: $abstract,
                language: $language,
                conference: $conference,
                topic: $topic,
                type: $type,
                duration: $duration,
            }) {
                submission {
                    id,
                    title
                    abstract
                }
                errors {
                    messages
                    field
                }
            }
        }
        """,
        variables=variables,
    ), variables


def _submit_tutorial(client, conference, **kwargs):
    talk = SubmissionFactory.build(
        type=SubmissionType.objects.get_or_create(name='tutorial')[0]
    )

    defaults = {
        'title': talk.title,
        'abstract': talk.abstract,
        'elevator_pitch': talk.elevator_pitch,
        'notes': talk.notes,
        'language': 'it',
        'conference': conference.code,
        'topic': conference.topics.first().id,
        'type': talk.type.id,
        'duration': conference.durations.first().id,
    }

    variables = {**defaults, **kwargs}

    return client.query(
        """
        mutation($conference: ID!, $topic: ID!, $title: String!, $abstract: String!, $language: ID!, $type: ID!, $duration: ID!) {
            sendSubmission(input: {
                title: $title,
                abstract: $abstract,
                language: $language,
                conference: $conference,
                topic: $topic,
                type: $type,
                duration: $duration,
            }) {
                submission {
                    id,
                    title
                    abstract
                }
                errors {
                    messages
                    field
                }
            }
        }
        """,
        variables=variables,
    ), variables


@mark.django_db
def test_submit_talk(graphql_client, user, conference_factory):
    graphql_client.force_login(user)

    conference = conference_factory(
        topics=('my-topic',),
        languages=('it',),
        submission_types=('talk',),
        active_cfp=True,
        durations=('50',),
    )

    resp, variables = _submit_talk(
        graphql_client,
        conference,
    )

    assert resp['data']['sendSubmission']['submission'] is not None, resp
    assert resp['data']['sendSubmission']['errors'] == []

    assert resp['data']['sendSubmission']['submission']['title'] == variables['title']
    assert resp['data']['sendSubmission']['submission']['abstract'] == variables['abstract']

    talk = Submission.objects.get(id=resp['data']['sendSubmission']['submission']['id'])

    assert talk.title == variables['title']
    assert talk.abstract == variables['abstract']
    assert talk.language.code == 'it'
    assert talk.topic.name == 'my-topic'
    assert talk.conference == conference
    assert talk.speaker == user


@mark.django_db
def test_submit_talk_with_not_valid_conf_language(graphql_client, user, conference_factory):
    graphql_client.force_login(user)

    conference = conference_factory(
        topics=('my-topic',),
        languages=('it',),
        submission_types=('talk',),
        durations=('50',),
        active_cfp=True,
    )

    resp, _ = _submit_talk(graphql_client, conference, language='en')

    assert resp['data']['sendSubmission']['submission'] is None
    assert resp['data']['sendSubmission']['errors'][0]['messages'] == ['English (en) is not an allowed language']
    assert resp['data']['sendSubmission']['errors'][0]['field'] == 'language'


@mark.django_db
def test_cannot_use_duration_if_submission_type_is_not_allowed(
    graphql_client,
    user,
    conference_factory,
    duration_factory,
    submission_type_factory
):
    graphql_client.force_login(user)

    talk_type = submission_type_factory(name='talk')
    tutorial_type = submission_type_factory(name='tutorial')

    conference = conference_factory(
        topics=('my-topic',),
        languages=('it',),
        submission_types=('talk', 'tutorial'),
        active_cfp=True,
    )

    duration1 = duration_factory(conference=conference)
    duration1.allowed_submission_types.add(talk_type)

    duration2 = duration_factory(conference=conference)
    duration2.allowed_submission_types.add(tutorial_type)

    resp, _ = _submit_talk(graphql_client, conference, type=talk_type.id, duration=duration2.id)

    assert resp['data']['sendSubmission']['submission'] is None
    assert (
        resp['data']['sendSubmission']['errors'][0]['messages']
        ==
        [f'Duration {str(duration2)} is not an allowed for the submission type {str(talk_type)}']
    )
    assert resp['data']['sendSubmission']['errors'][0]['field'] == 'duration'


@mark.django_db
def test_submit_talk_with_duration_id_of_another_conf(graphql_client, user, conference_factory, duration_factory):
    graphql_client.force_login(user)

    another_conf_duration = duration_factory()

    conference = conference_factory(
        topics=('my-topic',),
        languages=('it',),
        submission_types=('talk',),
        durations=('50',),
        active_cfp=True,
    )

    resp, _ = _submit_talk(graphql_client, conference, duration=another_conf_duration.id)

    assert resp['data']['sendSubmission']['submission'] is None
    assert (
        resp['data']['sendSubmission']['errors'][0]['messages']
        ==
        [f'{str(another_conf_duration)} is not an allowed duration type']
    )
    assert resp['data']['sendSubmission']['errors'][0]['field'] == 'duration'


@mark.django_db
def test_submit_talk_with_not_valid_conf_topic(graphql_client, user, conference_factory, topic_factory):
    graphql_client.force_login(user)

    conference = conference_factory(
        topics=('my-topic',),
        languages=('it',),
        submission_types=('talk',),
        active_cfp=True,
        durations=('50',),
    )
    topic = topic_factory(name='random topic')

    resp, _ = _submit_talk(graphql_client, conference, topic=topic.id)

    assert resp['data']['sendSubmission']['submission'] is None
    assert resp['data']['sendSubmission']['errors'][0]['messages'] == ['random topic is not a valid topic']
    assert resp['data']['sendSubmission']['errors'][0]['field'] == 'topic'


@mark.django_db
def test_submit_talk_with_not_valid_submission_type(graphql_client, user, conference_factory, topic_factory):
    graphql_client.force_login(user)

    conference = conference_factory(
        topics=('my-topic',),
        languages=('it',),
        submission_types=('tutorial',),
        active_cfp=True,
        durations=('50',),
    )

    resp, _ = _submit_talk(graphql_client, conference)

    assert resp['data']['sendSubmission']['submission'] is None
    assert resp['data']['sendSubmission']['errors'][0]['messages'] == ['talk is not an allowed submission type']
    assert resp['data']['sendSubmission']['errors'][0]['field'] == 'type'


@mark.django_db
def test_cannot_propose_a_talk_as_unlogged_user(graphql_client, conference_factory):
    conference = conference_factory(
        topics=('my-topic',),
        languages=('it',),
        submission_types=('talk',),
        durations=('50',),
    )

    resp, _ = _submit_talk(graphql_client, conference)

    assert resp['errors'][0]['message'] == 'User not logged in'
    assert resp['data']['sendSubmission'] is None


@mark.django_db
def test_cannot_propose_a_talk_if_the_cfp_is_not_open(graphql_client, user, conference_factory):
    graphql_client.force_login(user)

    now = timezone.now()

    conference = conference_factory(
        topics=('friends',),
        languages=('it',),
        active_cfp=False,
        submission_types=('talk',),
        durations=('50',),
    )

    resp, _ = _submit_talk(graphql_client, conference)

    assert resp['data']['sendSubmission']['errors'][0]['messages'] == ['The call for papers is not open!']
    assert resp['data']['sendSubmission']['errors'][0]['field'] == '__all__'
    assert resp['data']['sendSubmission']['submission'] is None


@mark.django_db
def test_cannot_propose_a_talk_if_a_cfp_is_not_specified(graphql_client, user, conference_factory):
    graphql_client.force_login(user)

    conference = conference_factory(
        topics=('friends',),
        languages=('it',),
        submission_types=('talk',),
        durations=('50',),
    )

    resp, _ = _submit_talk(graphql_client, conference)

    assert resp['data']['sendSubmission']['errors'][0]['messages'] == ['The call for papers is not open!']
    assert resp['data']['sendSubmission']['errors'][0]['field'] == '__all__'
    assert resp['data']['sendSubmission']['submission'] is None


@mark.django_db
def test_same_user_can_propose_multiple_talks_to_the_same_conference(graphql_client, user, conference_factory):
    graphql_client.force_login(user)

    conference = conference_factory(
        topics=('friends',),
        languages=('it',),
        active_cfp=True,
        submission_types=('talk',),
        durations=('50',),
    )

    resp, _ = _submit_talk(graphql_client, conference, title='My first talk')

    assert resp['data']['sendSubmission']['errors'] == []
    assert resp['data']['sendSubmission']['submission']['title'] == 'My first talk'

    assert user.submissions.filter(conference=conference).count() == 1

    resp, _ = _submit_talk(graphql_client, conference, title='Another talk')

    assert resp['data']['sendSubmission']['errors'] == []
    assert resp['data']['sendSubmission']['submission']['title'] == 'Another talk'

    assert user.submissions.filter(conference=conference).count() == 2


@mark.django_db
def test_submit_tutorial(graphql_client, user, conference_factory):
    graphql_client.force_login(user)

    conference = conference_factory(
        topics=('friends',),
        languages=('it',),
        active_cfp=True,
        submission_types=('talk', 'tutorial'),
        durations=('50',),
    )

    resp, _ = _submit_tutorial(graphql_client, conference, title='My first tutorial')

    assert resp['data']['sendSubmission']['errors'] == []
    assert resp['data']['sendSubmission']['submission']['title'] == 'My first tutorial'

    assert user.submissions.filter(conference=conference).count() == 1


@mark.django_db
def test_submit_tutorial_and_talk_to_the_same_conference(graphql_client, user, conference_factory):
    graphql_client.force_login(user)

    conference = conference_factory(
        topics=('friends',),
        languages=('it',),
        active_cfp=True,
        submission_types=('talk', 'tutorial'),
        durations=('50',),
    )

    resp, _ = _submit_tutorial(graphql_client, conference, title='My first tutorial')

    assert resp['data']['sendSubmission']['errors'] == []
    assert resp['data']['sendSubmission']['submission']['title'] == 'My first tutorial'

    assert user.submissions.filter(conference=conference).count() == 1

    resp, _ = _submit_talk(graphql_client, conference, title='My first talk')

    assert resp['data']['sendSubmission']['errors'] == []
    assert resp['data']['sendSubmission']['submission']['title'] == 'My first talk'

    assert user.submissions.filter(conference=conference).count() == 2


@mark.django_db
def test_same_user_can_submit_talks_to_different_conferences(graphql_client, user, conference_factory):
    graphql_client.force_login(user)

    conference1 = conference_factory(
        topics=('friends',),
        languages=('it',),
        active_cfp=True,
        submission_types=('talk',),
        durations=('50',),
    )

    conference2 = conference_factory(
        topics=('another-stuff',),
        languages=('it', 'en'),
        active_cfp=True,
        submission_types=('talk',),
        durations=('50',),
    )

    resp, _ = _submit_talk(graphql_client, conference1, title='My first talk')

    assert resp['data']['sendSubmission']['errors'] == []
    assert resp['data']['sendSubmission']['submission']['title'] == 'My first talk'

    assert user.submissions.filter(conference=conference1).count() == 1
    assert user.submissions.filter(conference=conference2).count() == 0

    resp, _ = _submit_talk(graphql_client, conference2, title='Another talk')

    assert resp['data']['sendSubmission']['errors'] == []
    assert resp['data']['sendSubmission']['submission']['title'] == 'Another talk'

    assert user.submissions.filter(conference=conference1).count() == 1
    assert user.submissions.filter(conference=conference2).count() == 1
