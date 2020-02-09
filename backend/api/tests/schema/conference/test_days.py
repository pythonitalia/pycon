from datetime import date, time

from pytest import mark


@mark.django_db
def test_get_days_always_returns_conference_day(conference_factory, graphql_client):
    conference = conference_factory(start=date(2020, 4, 2), end=date(2020, 4, 5))

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                days {
                    day
                    slots {
                        hour
                        duration
                    }
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["days"] == [
        {"day": "2020-04-02", "slots": []},
        {"day": "2020-04-03", "slots": []},
        {"day": "2020-04-04", "slots": []},
        {"day": "2020-04-05", "slots": []},
    ]


@mark.django_db
def test_get_days_with_configuration(
    conference_factory, day_factory, slot_factory, graphql_client
):
    conference = conference_factory(start=date(2020, 4, 2), end=date(2020, 4, 2))

    day = day_factory(conference=conference, day=date(2020, 4, 2))

    slot_factory(day=day, hour=time(8, 45), duration=60)

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                days {
                    day
                    slots {
                        hour
                        duration
                    }
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["days"] == [
        {"day": "2020-04-02", "slots": [{"hour": "08:45:00", "duration": 60}]}
    ]


@mark.django_db
def test_add_slot_creates_day(conference_factory, day_factory, graphql_client):
    conference = conference_factory(start=date(2020, 4, 2), end=date(2020, 4, 2))

    resp = graphql_client.query(
        """
        mutation AddScheduleSlot($code: ID!, $day: Date!, $duration: Int!) {
            addScheduleSlot(conference: $code, day: $day, duration: $duration) {
                ... on Day {
                    day
                    slots {
                        hour
                        duration
                    }
                }
            }
        }
        """,
        variables={"code": conference.code, "day": "2020-04-02", "duration": 60},
    )

    assert "errors" not in resp

    assert resp["data"]["addScheduleSlot"] == {
        "day": "2020-04-02",
        "slots": [{"hour": "08:45:00", "duration": 60}],
    }

    assert conference.days.count() == 1


@mark.django_db
def test_add_slot_add_slot(
    conference_factory, day_factory, slot_factory, graphql_client
):
    conference = conference_factory(start=date(2020, 4, 2), end=date(2020, 4, 2))

    day = day_factory(conference=conference, day=date(2020, 4, 2))

    slot_factory(day=day, hour=time(8, 45), duration=60)

    resp = graphql_client.query(
        """
        mutation AddScheduleSlot($code: ID!, $day: Date!, $duration: Int!) {
            addScheduleSlot(conference: $code, day: $day, duration: $duration) {
                ... on Day {
                    day
                    slots {
                        hour
                        duration
                    }
                }
            }
        }
        """,
        variables={"code": conference.code, "day": "2020-04-02", "duration": 45},
    )

    assert "errors" not in resp

    assert resp["data"]["addScheduleSlot"] == {
        "day": "2020-04-02",
        "slots": [
            {"hour": "08:45:00", "duration": 60},
            {"hour": "09:45:00", "duration": 45},
        ],
    }

    assert conference.days.count() == 1
