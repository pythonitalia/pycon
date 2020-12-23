from datetime import date, datetime, time

import pytz
from api.helpers.ids import encode_hashid
from pytest import mark


@mark.django_db
def test_get_days_with_configuration(
    conference_factory,
    day_factory,
    slot_factory,
    schedule_item_factory,
    admin_graphql_client,
):
    conference = conference_factory(
        start=datetime(2020, 4, 2, tzinfo=pytz.UTC),
        end=datetime(2020, 4, 2, tzinfo=pytz.UTC),
    )

    day = day_factory(conference=conference, day=date(2020, 4, 2))
    slot = slot_factory(day=day, hour=time(8, 45), duration=60)
    item = schedule_item_factory(slot=slot, submission=None)

    resp = admin_graphql_client.query(
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
    conference_factory, day_factory, slot_factory, room, admin_graphql_client
):
    conference = conference_factory(
        start=datetime(2020, 4, 2, tzinfo=pytz.UTC),
        end=datetime(2020, 4, 2, tzinfo=pytz.UTC),
    )

    day = day_factory(conference=conference, day=date(2020, 4, 2))
    slot = slot_factory(day=day, hour=time(8, 45), duration=60)

    resp = admin_graphql_client.query(
        """
        mutation($input: UpdateOrCreateSlotItemInput!) {
            updateOrCreateSlotItem(input: $input) {
                ... on UpdateOrCreateSlotItemResult {
                    updatedSlots {
                        items {
                            type
                            title
                            rooms {
                                id
                            }
                        }
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
    assert resp["data"]["updateOrCreateSlotItem"]["updatedSlots"][0]["items"] == [
        {"title": "Custom slot", "type": "custom", "rooms": [{"id": str(room.id)}]}
    ]


@mark.django_db
def test_add_custom_item_from_submission(
    conference_factory,
    day_factory,
    slot_factory,
    room,
    submission,
    admin_graphql_client,
):
    conference = conference_factory(
        start=datetime(2020, 4, 2, tzinfo=pytz.UTC),
        end=datetime(2020, 4, 2, tzinfo=pytz.UTC),
    )

    day = day_factory(conference=conference, day=date(2020, 4, 2))
    slot = slot_factory(day=day, hour=time(8, 45), duration=60)

    resp = admin_graphql_client.query(
        """
        mutation($input: UpdateOrCreateSlotItemInput!) {
            updateOrCreateSlotItem(input: $input) {
                ... on UpdateOrCreateSlotItemResult {
                    updatedSlots {
                        items {
                            type
                            title
                        }
                }
            }
        }
                    }
        """,
        variables={
            "input": {
                "slotId": slot.id,
                "submissionId": encode_hashid(submission.id),
                "rooms": [room.id],
            }
        },
    )

    assert "errors" not in resp
    assert resp["data"]["updateOrCreateSlotItem"]["updatedSlots"][0]["items"] == [
        {"title": submission.title, "type": "submission"}
    ]


@mark.django_db
def test_edit_item(
    conference_factory,
    day_factory,
    slot_factory,
    room,
    admin_graphql_client,
    schedule_item_factory,
):
    conference = conference_factory(
        start=datetime(2020, 4, 2, tzinfo=pytz.UTC),
        end=datetime(2020, 4, 2, tzinfo=pytz.UTC),
    )

    day = day_factory(conference=conference, day=date(2020, 4, 2))
    slot = slot_factory(day=day, hour=time(8, 45), duration=60)
    slot_2 = slot_factory(day=day, hour=time(8, 45), duration=60)
    item = schedule_item_factory(slot=slot, submission=None, type="submission")

    resp = admin_graphql_client.query(
        """
        mutation($input: UpdateOrCreateSlotItemInput!) {
            updateOrCreateSlotItem(input: $input) {
                ... on UpdateOrCreateSlotItemResult {
                    updatedSlots {
                        id
                        items {
                            id
                            type
                            title
                        }
                    }
                }
            }
        }
        """,
        variables={
            "input": {"slotId": slot_2.id, "itemId": item.id, "rooms": [room.id]}
        },
    )

    assert "errors" not in resp

    updated_slots = resp["data"]["updateOrCreateSlotItem"]["updatedSlots"]

    assert updated_slots[0]["id"] == str(slot.id)
    assert updated_slots[1]["id"] == str(slot_2.id)
    assert updated_slots[1]["items"] == [
        {"id": str(item.id), "title": item.title, "type": item.type}
    ]
