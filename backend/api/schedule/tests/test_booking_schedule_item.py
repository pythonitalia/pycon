from pytest import mark

from schedule.models import ScheduleItem


def _release_schedule_item_booking(graphql_client, conference, schedule_item_booking):
    return graphql_client.query(
        """
    mutation($conference: String!, $id: ID!) {
        releaseScheduleItemBooking(conference: $conference, id: $id) {
            __typename

            ... on ScheduleItemBookingStatus {
                scheduleItem {
                    isBooked
                    canBook
                }
            }

            ... on ReleaseScheduleItemBookingError {
                message
            }
        }
    }
    """,
        variables={
            "id": schedule_item_booking.schedule_item.id,
            "conference": conference.code,
        },
    )


def _book_schedule_item(graphql_client, conference, schedule_item):
    return graphql_client.query(
        """
    mutation($conference: String!, $id: ID!) {
        bookScheduleItem(conference: $conference, id: $id) {
            __typename

            ... on ScheduleItemBookingStatus {
                scheduleItem {
                    isBooked
                    canBook
                }
            }

            ... on BookScheduleItemError {
                message
            }
        }
    }
    """,
        variables={"id": schedule_item.id, "conference": conference.code},
    )


@mark.django_db
def test_cannot_book_schedule_item_unlogged(graphql_client, schedule_item_factory):
    schedule_item = schedule_item_factory(rooms=("test"))
    resp = _book_schedule_item(graphql_client, schedule_item.conference, schedule_item)

    assert resp["errors"]
    assert resp["errors"][0]["message"] == "User not logged in"


@mark.django_db
def test_book_schedule_item(user, graphql_client, schedule_item_factory, mocker):
    mocker.patch("users.models.user_has_admission_ticket").return_value = True

    schedule_item = schedule_item_factory(
        rooms=("test",), type=ScheduleItem.TYPES.training
    )
    graphql_client.force_login(user)

    resp = _book_schedule_item(graphql_client, schedule_item.conference, schedule_item)

    assert resp["data"]["bookScheduleItem"]["__typename"] == "ScheduleItemBookingStatus"
    assert resp["data"]["bookScheduleItem"]["scheduleItem"] == {
        "isBooked": True,
        "canBook": True,
    }

    assert schedule_item.bookings.filter(user=user).exists()


@mark.django_db
def test_user_can_book_multiple_times_but_counts_only_once(
    user, graphql_client, schedule_item_factory, mocker
):
    mocker.patch("users.models.user_has_admission_ticket").return_value = True

    schedule_item = schedule_item_factory(
        rooms=("test",), type=ScheduleItem.TYPES.training
    )
    graphql_client.force_login(user)

    resp = _book_schedule_item(graphql_client, schedule_item.conference, schedule_item)

    assert resp["data"]["bookScheduleItem"]["__typename"] == "ScheduleItemBookingStatus"
    assert resp["data"]["bookScheduleItem"]["scheduleItem"] == {
        "isBooked": True,
        "canBook": True,
    }

    assert schedule_item.bookings.count() == 1

    resp = _book_schedule_item(graphql_client, schedule_item.conference, schedule_item)

    assert resp["data"]["bookScheduleItem"]["__typename"] == "ScheduleItemBookingStatus"
    assert resp["data"]["bookScheduleItem"]["scheduleItem"] == {
        "isBooked": True,
        "canBook": True,
    }

    assert schedule_item.bookings.count() == 1


@mark.django_db
def test_cannot_book_a_full_schedule_item(
    user, graphql_client, schedule_item_factory, mocker
):
    mocker.patch("users.models.user_has_admission_ticket").return_value = True

    schedule_item = schedule_item_factory(
        maximum_capacity=0, type=ScheduleItem.TYPES.training
    )
    graphql_client.force_login(user)

    resp = _book_schedule_item(graphql_client, schedule_item.conference, schedule_item)

    assert resp["data"]["bookScheduleItem"]["__typename"] == "BookScheduleItemError"
    assert resp["data"]["bookScheduleItem"]["message"] == "No seats left"


@mark.django_db
@mark.parametrize("has_ticket", [True, False])
def test_can_only_book_if_the_user_has_a_ticket(
    user, graphql_client, schedule_item_factory, has_ticket, mocker
):
    mocker.patch("users.models.user_has_admission_ticket").return_value = has_ticket

    schedule_item = schedule_item_factory(
        maximum_capacity=10, type=ScheduleItem.TYPES.training
    )
    graphql_client.force_login(user)

    resp = _book_schedule_item(graphql_client, schedule_item.conference, schedule_item)

    if not has_ticket:
        assert resp["data"]["bookScheduleItem"]["__typename"] == "BookScheduleItemError"
        assert (
            resp["data"]["bookScheduleItem"]["message"]
            == "You need a ticket to book a seat"
        )
    else:
        assert (
            resp["data"]["bookScheduleItem"]["__typename"]
            == "ScheduleItemBookingStatus"
        )
        assert resp["data"]["bookScheduleItem"]["scheduleItem"] == {
            "isBooked": True,
            "canBook": True,
        }


@mark.django_db
def test_can_only_book_trainings(user, graphql_client, schedule_item_factory, mocker):
    mocker.patch("users.models.user_has_admission_ticket").return_value = True

    schedule_item = schedule_item_factory(
        maximum_capacity=0, type=ScheduleItem.TYPES.submission
    )
    graphql_client.force_login(user)

    resp = _book_schedule_item(graphql_client, schedule_item.conference, schedule_item)

    assert resp["data"]["bookScheduleItem"]["__typename"] == "BookScheduleItemError"
    assert (
        resp["data"]["bookScheduleItem"]["message"]
        == "You cannot book this type of event"
    )


@mark.django_db
def test_release_booking(user, graphql_client, schedule_item_booking_factory):
    graphql_client.force_login(user)

    booking = schedule_item_booking_factory(
        user=user, schedule_item__type=ScheduleItem.TYPES.training,
    )

    resp = _release_schedule_item_booking(
        graphql_client, booking.schedule_item.conference, booking
    )

    assert (
        resp["data"]["releaseScheduleItemBooking"]["__typename"]
        == "ScheduleItemBookingStatus"
    )
    assert resp["data"]["releaseScheduleItemBooking"]["scheduleItem"] == {
        "isBooked": False,
        "canBook": True,
    }


@mark.django_db
def test_cannot_release_someone_else_booking(
    user_factory, graphql_client, schedule_item_booking_factory
):
    user_a = user_factory()
    user_b = user_factory()

    graphql_client.force_login(user_a)

    booking = schedule_item_booking_factory(
        user=user_b, schedule_item__type=ScheduleItem.TYPES.training,
    )

    resp = _release_schedule_item_booking(
        graphql_client, booking.schedule_item.conference, booking
    )

    assert (
        resp["data"]["releaseScheduleItemBooking"]["__typename"]
        == "ReleaseScheduleItemBookingError"
    )
    assert resp["data"]["releaseScheduleItemBooking"]["message"] == "No booking found"


@mark.django_db
def test_cannot_release_booking_of_another_conference(
    user, graphql_client, schedule_item_booking_factory, conference
):
    graphql_client.force_login(user)

    booking = schedule_item_booking_factory(user=user)

    resp = _release_schedule_item_booking(graphql_client, conference, booking)

    assert (
        resp["data"]["releaseScheduleItemBooking"]["__typename"]
        == "ReleaseScheduleItemBookingError"
    )
    assert resp["data"]["releaseScheduleItemBooking"]["message"] == "No booking found"


@mark.django_db
def test_cannot_release_booking_unlogged(graphql_client, schedule_item_booking_factory):
    booking = schedule_item_booking_factory(
        schedule_item__type=ScheduleItem.TYPES.training,
    )

    resp = _release_schedule_item_booking(
        graphql_client, booking.schedule_item.conference, booking
    )

    assert resp["errors"]
    assert resp["errors"][0]["message"] == "User not logged in"


@mark.django_db
def test_get_booked_schedule_item(
    graphql_client, user, conference, schedule_item_booking_factory
):
    booking = schedule_item_booking_factory(
        user=user,
        schedule_item__type=ScheduleItem.TYPES.training,
        schedule_item__conference=conference,
        schedule_item__submission__conference=conference,
    )
    graphql_client.force_login(user)

    resp = graphql_client.query(
        """
        query($conference: String!, $talk: String!) {
            conference(code: $conference) {
                talk(slug: $talk) {
                    isBooked
                }
            }
        }
    """,
        variables={
            "conference": booking.schedule_item.conference.code,
            "talk": booking.schedule_item.slug,
        },
    )

    assert resp["data"]["conference"]["talk"]["isBooked"] is True


@mark.django_db
def test_get_booked_schedule_item_as_unlogged(
    graphql_client, user, conference, schedule_item_booking_factory
):
    booking = schedule_item_booking_factory(
        user=user,
        schedule_item__type=ScheduleItem.TYPES.training,
        schedule_item__conference=conference,
        schedule_item__submission__conference=conference,
    )

    resp = graphql_client.query(
        """
        query($conference: String!, $talk: String!) {
            conference(code: $conference) {
                talk(slug: $talk) {
                    isBooked
                }
            }
        }
    """,
        variables={
            "conference": booking.schedule_item.conference.code,
            "talk": booking.schedule_item.slug,
        },
    )

    assert resp["data"]["conference"]["talk"]["isBooked"] is False


@mark.django_db
def test_get_booked_schedule_item_when_not_booked(
    graphql_client, user_factory, conference, schedule_item_booking_factory
):
    user_a = user_factory()
    user_b = user_factory()

    schedule_item_booking_factory(
        user=user_b,
        schedule_item__type=ScheduleItem.TYPES.training,
        schedule_item__conference=conference,
        schedule_item__submission__conference=conference,
    )
    booking = schedule_item_booking_factory(
        user=user_a,
        schedule_item__type=ScheduleItem.TYPES.training,
        schedule_item__conference=conference,
        schedule_item__submission__conference=conference,
    )

    graphql_client.force_login(user_b)

    resp = graphql_client.query(
        """
        query($conference: String!, $talk: String!) {
            conference(code: $conference) {
                talk(slug: $talk) {
                    isBooked
                }
            }
        }
    """,
        variables={
            "conference": booking.schedule_item.conference.code,
            "talk": booking.schedule_item.slug,
        },
    )

    assert resp["data"]["conference"]["talk"]["isBooked"] is False


@mark.django_db
@mark.parametrize("has_space", [True, False])
def test_get_schedule_item_has_free_spot(
    graphql_client, schedule_item_factory, has_space
):
    schedule_item = schedule_item_factory(
        type=ScheduleItem.TYPES.training, maximum_capacity=10 if has_space else 0
    )

    resp = graphql_client.query(
        """
        query($conference: String!, $talk: String!) {
            conference(code: $conference) {
                talk(slug: $talk) {
                    hasFreeSpot
                }
            }
        }
    """,
        variables={
            "conference": schedule_item.conference.code,
            "talk": schedule_item.slug,
        },
    )

    assert resp["data"]["conference"]["talk"]["hasFreeSpot"] is has_space
