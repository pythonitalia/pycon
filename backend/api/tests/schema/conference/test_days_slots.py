from datetime import date, time

from pytest import mark


@mark.django_db
def test_get_days_with_configuration(
    conference_factory, day_factory, slot_factory, schedule_item_factory, graphql_client
):
    conference = conference_factory(start=date(2020, 4, 2), end=date(2020, 4, 2))

    day = day_factory(conference=conference, day=date(2020, 4, 2))
    slot = slot_factory(day=day, hour=time(8, 45), duration=60, offset=0)
    item = schedule_item_factory(slot=slot)

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


@mark.django_db
def test_add_custom_item(
    conference_factory, day_factory, slot_factory, room, graphql_client
):
    conference = conference_factory(start=date(2020, 4, 2), end=date(2020, 4, 2))

    day = day_factory(conference=conference, day=date(2020, 4, 2))
    slot = slot_factory(day=day, hour=time(8, 45), duration=60, offset=0)

    resp = graphql_client.query(
        """
        mutation($input: UpdateOrCreateSlotItemInput!) {
            updateOrCreateSlotItem(input: $input) {
                ... on ScheduleSlot {
                    items {
                        type
                        title
                    }
                }
            }
        }
        """,
        variables={
            "input": {"slotId": slot.id, "title": "Custom slot", "rooms": [room.id]}
        },
    )

    assert "errors" not in resp
    assert resp["data"]["updateOrCreateSlotItem"]["items"] == [
        {"title": "Custom slot", "type": "custom"}
    ]
