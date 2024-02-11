from datetime import date, datetime, time

import pytz
from pytest import mark


@mark.django_db
def test_get_days_with_configuration(
    conference_factory,
    day_factory,
    slot_factory,
    schedule_item_factory,
    graphql_client,
):
    conference = conference_factory(
        start=datetime(2020, 4, 2, tzinfo=pytz.UTC),
        end=datetime(2020, 4, 2, tzinfo=pytz.UTC),
    )

    day = day_factory(conference=conference, day=date(2020, 4, 2))
    slot = slot_factory(day=day, hour=time(8, 45), duration=60)
    item = schedule_item_factory(conference=conference, slot=slot, submission=None)

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                days {
                    day
                    slots {
                        items {
                            type
                            title
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
        {"title": item.title, "type": item.type}
    ]
