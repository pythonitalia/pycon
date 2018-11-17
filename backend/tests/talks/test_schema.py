from pytest import mark

from django.utils import timezone

from talks.models import Talk

from .factories import TalkFactory


def _propose_talk(client, conference, **kwargs):
    talk = TalkFactory.build()

    defaults = {
        'title': talk.title,
        'abstract': talk.abstract,
        'elevator_pitch': talk.elevator_pitch,
        'notes': talk.notes,
        'language': 'it',
        'conference': conference.code,
        'topic': conference.topics.first().id,
    }

    variables = {**defaults, **kwargs}

    return client.query(
        """
        mutation($conference: ID!, $topic: ID!, $title: String!, $abstract: String!, $language: ID!) {
            proposeTalk(input: {
                title: $title,
                abstract: $abstract,
                language: $language,
                conference: $conference,
                topic: $topic,
            }) {
                talk {
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
def test_propose_talk(graphql_client, user, conference_factory):
    graphql_client.force_login(user)

    conference = conference_factory(topics=('my-topic',), languages=('it',), active_cfp=True)

    resp, variables = _propose_talk(
        graphql_client,
        conference,
    )

    assert resp['data']['proposeTalk']['talk'] is not None
    assert resp['data']['proposeTalk']['errors'] == []

    assert resp['data']['proposeTalk']['talk']['title'] == variables['title']
    assert resp['data']['proposeTalk']['talk']['abstract'] == variables['abstract']

    talk = Talk.objects.get(id=resp['data']['proposeTalk']['talk']['id'])

    assert talk.title == variables['title']
    assert talk.abstract == variables['abstract']
    assert talk.language.code == 'it'
    assert talk.topic.name == 'my-topic'
    assert talk.conference == conference
    assert talk.speaker == user


@mark.django_db
def test_propose_talk_with_not_valid_conf_language(graphql_client, user, conference_factory):
    graphql_client.force_login(user)

    conference = conference_factory(topics=('my-topic',), languages=('it',), active_cfp=True)

    resp, _ = _propose_talk(graphql_client, conference, language='en')

    assert resp['data']['proposeTalk']['talk'] is None
    assert resp['data']['proposeTalk']['errors'][0]['messages'] == ['English (en) is not an allowed language']
    assert resp['data']['proposeTalk']['errors'][0]['field'] == 'language'


@mark.django_db
def test_propose_talk_with_not_valid_conf_topic(graphql_client, user, conference_factory, topic_factory):
    graphql_client.force_login(user)

    conference = conference_factory(topics=('my-topic',), languages=('it',), active_cfp=True)
    topic = topic_factory(name='random topic')

    resp, _ = _propose_talk(graphql_client, conference, topic=topic.id)

    assert resp['data']['proposeTalk']['talk'] is None
    assert resp['data']['proposeTalk']['errors'][0]['messages'] == ['random topic is not a valid topic']
    assert resp['data']['proposeTalk']['errors'][0]['field'] == 'topic'


@mark.django_db
def test_cannot_propose_a_talk_as_unlogged_user(graphql_client, conference_factory):
    conference = conference_factory(topics=('my-topic',), languages=('it',))

    resp, _ = _propose_talk(graphql_client, conference)

    assert resp['errors'][0]['message'] == 'User not logged in'
    assert resp['data']['proposeTalk'] is None


@mark.django_db
def test_cannot_propose_a_talk_if_the_cfp_is_not_open(graphql_client, user, conference_factory):
    graphql_client.force_login(user)

    now = timezone.now()

    conference = conference_factory(
        topics=('friends',),
        languages=('it',),
        active_cfp=False
    )

    resp, _ = _propose_talk(graphql_client, conference)

    assert resp['data']['proposeTalk']['errors'][0]['messages'] == ['The call for papers is not open!']
    assert resp['data']['proposeTalk']['errors'][0]['field'] == '__all__'
    assert resp['data']['proposeTalk']['talk'] is None


@mark.django_db
def test_cannot_propose_a_talk_if_a_cfp_is_not_specified(graphql_client, user, conference_factory):
    graphql_client.force_login(user)

    conference = conference_factory(
        topics=('friends',),
        languages=('it',),
    )

    resp, _ = _propose_talk(graphql_client, conference)

    assert resp['data']['proposeTalk']['errors'][0]['messages'] == ['The call for papers is not open!']
    assert resp['data']['proposeTalk']['errors'][0]['field'] == '__all__'
    assert resp['data']['proposeTalk']['talk'] is None


@mark.django_db
def test_same_user_can_propose_multiple_talks_to_the_same_conference(graphql_client, user, conference_factory):
    graphql_client.force_login(user)

    conference = conference_factory(
        topics=('friends',),
        languages=('it',),
        active_cfp=True
    )

    resp, _ = _propose_talk(graphql_client, conference, title='My first talk')

    assert resp['data']['proposeTalk']['errors'] == []
    assert resp['data']['proposeTalk']['talk']['title'] == 'My first talk'

    assert user.talks.filter(conference=conference).count() == 1

    resp, _ = _propose_talk(graphql_client, conference, title='Another talk')

    assert resp['data']['proposeTalk']['errors'] == []
    assert resp['data']['proposeTalk']['talk']['title'] == 'Another talk'

    assert user.talks.filter(conference=conference).count() == 2


@mark.django_db
def test_same_user_can_propose_talks_to_different_conferences(graphql_client, user, conference_factory):
    graphql_client.force_login(user)

    conference1 = conference_factory(
        topics=('friends',),
        languages=('it',),
        active_cfp=True
    )

    conference2 = conference_factory(
        topics=('another-stuff',),
        languages=('it', 'en'),
        active_cfp=True
    )

    resp, _ = _propose_talk(graphql_client, conference1, title='My first talk')

    assert resp['data']['proposeTalk']['errors'] == []
    assert resp['data']['proposeTalk']['talk']['title'] == 'My first talk'

    assert user.talks.filter(conference=conference1).count() == 1
    assert user.talks.filter(conference=conference2).count() == 0

    resp, _ = _propose_talk(graphql_client, conference2, title='Another talk')

    assert resp['data']['proposeTalk']['errors'] == []
    assert resp['data']['proposeTalk']['talk']['title'] == 'Another talk'

    assert user.talks.filter(conference=conference1).count() == 1
    assert user.talks.filter(conference=conference2).count() == 1
