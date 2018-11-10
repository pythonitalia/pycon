from pytest import mark

from talks.models import Talk


def _propose_talk(client, title, abstract, language, conference, topic):
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
        variables={
            'title': title,
            'abstract': abstract,
            'language': language,
            'conference': conference.code,
            'topic': topic.id,
        }
    )


@mark.django_db
def test_propose_talk(graphql_client, user, conference_factory):
    graphql_client.force_login(user)

    conference = conference_factory(topics=('my-topic',), languages=('it',))
    topic = conference.topics.first()

    resp = _propose_talk(graphql_client, 'Test title', 'Abstract content', 'it', conference, topic)

    assert resp['data']['proposeTalk']['talk'] is not None
    assert resp['data']['proposeTalk']['errors'] == []

    assert resp['data']['proposeTalk']['talk']['title'] == 'Test title'
    assert resp['data']['proposeTalk']['talk']['abstract'] == 'Abstract content'

    talk = Talk.objects.get(id=resp['data']['proposeTalk']['talk']['id'])

    assert talk.title == 'Test title'
    assert talk.abstract == 'Abstract content'
    assert talk.language.code == 'it'
    assert talk.topic.name == 'my-topic'
    assert talk.conference == conference
    assert talk.owner == user


@mark.django_db
def test_propose_talk_with_not_valid_conf_language(graphql_client, user, conference_factory):
    graphql_client.force_login(user)

    conference = conference_factory(topics=('my-topic',), languages=('it',))
    topic = conference.topics.first()

    resp = _propose_talk(graphql_client, 'Test title', 'Abstract', 'en', conference, topic)

    assert resp['data']['proposeTalk']['talk'] is None
    assert resp['data']['proposeTalk']['errors'][0]['messages'] == [f'English (en) is not an allowed language for the conference {conference.code}']
    assert resp['data']['proposeTalk']['errors'][0]['field'] == 'language'


@mark.django_db
def test_propose_talk_with_not_valid_conf_topic(graphql_client, user, conference_factory, topic_factory):
    graphql_client.force_login(user)

    conference = conference_factory(topics=('my-topic',), languages=('it',))
    topic = topic_factory(name='random topic')

    resp = _propose_talk(graphql_client, 'Test title', 'Abstract', 'it', conference, topic)

    assert resp['data']['proposeTalk']['talk'] is None
    assert resp['data']['proposeTalk']['errors'][0]['messages'] == [f'random topic is not a valid topic for the conference {conference.code}']
    assert resp['data']['proposeTalk']['errors'][0]['field'] == 'topic'


@mark.django_db
def test_cannot_propose_a_talk_as_unlogged_user(graphql_client, conference_factory, topic_factory):
    conference = conference_factory(topics=('my-topic',), languages=('it',))
    topic = conference.topics.first()

    resp = _propose_talk(graphql_client, 'Test title', 'Abstract', 'it', conference, topic)

    assert resp['errors'][0]['message'] == 'User not logged in'
    assert resp['data']['proposeTalk'] is None
