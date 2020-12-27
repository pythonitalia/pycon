from pytest import mark


@mark.django_db
def test_get_rooms(conference, room_factory, graphql_client):
    room_1 = room_factory(conference=conference)

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                rooms {
                    name
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["rooms"] == [{"name": room_1.name}]
