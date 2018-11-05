from pytest import mark


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
