from datetime import date, time

import pytest


@pytest.mark.django_db
def test_get_my_favorite(
    user,
    graphql_client,
    conference_factory,
    day_factory,
    slot_factory,
    schedule_item_factory,
):
    graphql_client.force_login(user)

    conference = conference_factory(start=date(2020, 4, 2), end=date(2020, 4, 2))
    day = day_factory(conference=conference, day=date(2020, 4, 2))
    slot = slot_factory(day=day, hour=time(8, 45), duration=60)
    schedule_item_factory(slot=slot, subscribed_users=(user,))
    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                days {
                    day
                    slots {
                        items {
                            myFavorite
                        }
                    }
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["days"][0]["slots"][0]["items"] == [
        {"myFavorite": True}
    ]
