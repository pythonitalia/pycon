from datetime import date

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
                    scheduleConfiguration {
                        hour
                        duration
                        offset
                    }
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["days"] == [
        {"day": "2020-04-02", "scheduleConfiguration": []},
        {"day": "2020-04-03", "scheduleConfiguration": []},
        {"day": "2020-04-04", "scheduleConfiguration": []},
        {"day": "2020-04-05", "scheduleConfiguration": []},
    ]


@mark.django_db
def test_get_days_with_configuration(conference_factory, day_factory, graphql_client):
    conference = conference_factory(start=date(2020, 4, 2), end=date(2020, 4, 2))

    day_factory(
        conference=conference,
        day=date(2020, 4, 2),
        schedule_configuration=[
            {"hour": "08:45", "duration": 60, "offset": 0, "size": 45}
        ],
    )

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                days {
                    day
                    scheduleConfiguration {
                        hour
                        duration
                        offset
                        size
                    }
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["days"] == [
        {
            "day": "2020-04-02",
            "scheduleConfiguration": [
                {"hour": "08:45", "duration": 60, "offset": 0, "size": 45}
            ],
        }
    ]
