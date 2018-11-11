from pytest import mark

from django.utils import timezone


@mark.django_db
def test_get_conference_info(conference, ticket_factory, graphql_client):
    ticket = ticket_factory(conference=conference)

    resp = graphql_client.query(
        """
        query($code: String) {
            conference(code: $code) {
                id
                code
                name
                tickets {
                    id
                    name
                }
            }
        }
        """,
        variables={
            'code': conference.code
        }
    )

    assert 'errors' not in resp
    assert {
        'id': str(conference.id),
        'code': conference.code,
        'name': conference.name,
        'tickets': [
            {
                'id': str(ticket.id),
                'name': ticket.name,
            },
        ],
    } == resp['data']['conference']


@mark.django_db
def test_get_conference_deadlines_ordered_by_start_date(graphql_client, deadline_factory):
    now = timezone.now()

    deadline_voting = deadline_factory(
        start=now - timezone.timedelta(days=20),
        end=now - timezone.timedelta(days=15),
        type='voting'
    )

    conference = deadline_voting.conference

    deadline_cfp = deadline_factory(
        start=now - timezone.timedelta(days=1),
        end=now,
        conference=conference,
        type='cfp'
    )

    deadline_refund = deadline_factory(
        start=now - timezone.timedelta(days=14),
        end=now - timezone.timedelta(days=10),
        conference=conference,
        type='refund'
    )

    resp = graphql_client.query(
        """
        query($code: String) {
            conference(code: $code) {
                start
                end
                deadlines {
                    start
                    end
                    type
                }
            }
        }
        """,
        variables={
            'code': conference.code
        }
    )

    assert resp['data']['conference']['start'] == conference.start.isoformat()
    assert resp['data']['conference']['end'] == conference.end.isoformat()

    assert {
        'start': deadline_voting.start.isoformat(),
        'end': deadline_voting.end.isoformat(),
        'type': 'VOTING'
    } == resp['data']['conference']['deadlines'][0]

    assert {
        'start': deadline_refund.start.isoformat(),
        'end': deadline_refund.end.isoformat(),
        'type': 'REFUND'
    } == resp['data']['conference']['deadlines'][1]

    assert {
        'start': deadline_cfp.start.isoformat(),
        'end': deadline_cfp.end.isoformat(),
        'type': 'CFP'
    } == resp['data']['conference']['deadlines'][2]


@mark.django_db
def test_get_not_existent_conference_info(conference, graphql_client):
    resp = graphql_client.query(
        """
        {
            conference(code: "random-conference-code") {
                name
            }
        }
        """,
    )

    assert 'errors' in resp
    assert resp["errors"][0]["message"] == "Conference matching query does not exist."


@mark.django_db
def test_query_conference_audience_levels(graphql_client, conference, audience_level_factory):
    level1 = audience_level_factory()
    level2 = audience_level_factory()
    level3 = audience_level_factory()

    conference.audience_levels.add(level1, level2, level3)

    resp = graphql_client.query(
        """
        query($code: String) {
            conference(code: $code) {
                audienceLevels {
                    id
                    name
                }
            }
        }
        """,
        variables={
            'code': conference.code
        }
    )

    assert 'errors' not in resp

    assert {
        'name': level1.name,
        'id': str(level1.id)
    } in resp['data']['conference']['audienceLevels']

    assert {
        'name': level2.name,
        'id': str(level2.id)
    } in resp['data']['conference']['audienceLevels']

    assert {
        'name': level3.name,
        'id': str(level3.id)
    } in resp['data']['conference']['audienceLevels']
