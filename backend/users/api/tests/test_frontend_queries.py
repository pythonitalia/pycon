from datetime import date

from pytest import mark

from billing.tests.factories import BillingAddressFactory
from conferences.models import Deadline
from conferences.tests.factories import ConferenceFactory, DeadlineFactory
from visa.tests.factories import InvitationLetterRequestFactory

CURRENT_USER_QUERY = """
    query CurrentUser($conference: String!) {
      me {
        id
        name
        fullName
        email
        gender
        dateBirth
        country
        openToRecruiting
        openToNewsletter
        canEditSchedule
        isPythonItaliaMember
        userScheduleFavouritesCalendarUrl(conference: $conference)
        billingAddresses(conference: $conference) {
          isBusiness
          companyName
          userGivenName
          userFamilyName
          zipCode
          city
          address
          country
          vatId
          fiscalCode
          sdi
          pec
        }
      }
    }
"""


REQUEST_INVITATION_LETTER_PAGE_QUERY = """
    query RequestInvitationLetterPage($conference: String!) {
      conference(code: $conference) {
        id
        invitationLetterRequestDeadline: deadline(
          type: "invitation_letter_request"
        ) {
          id
          status
          start
        }
      }
      me {
        id
        hasAdmissionTicket(conference: $conference)
        invitationLetterRequest(conference: $conference) {
          id
          status
        }
      }
    }
"""


@mark.django_db
def test_frontend_current_user_query(graphql_client, django_assert_num_queries, user):
    conference = ConferenceFactory()
    user.name = "Patrick"
    user.full_name = "Patrick Arminio"
    user.gender = "male"
    user.date_birth = date(1990, 1, 1)
    user.country = "IT"
    user.open_to_recruiting = True
    user.open_to_newsletter = True
    user.is_staff = True
    user.save()
    billing_address = BillingAddressFactory(
        user=user,
        organizer=conference.organizer,
        company_name="Python Italia",
        user_given_name="Patrick",
        user_family_name="Arminio",
        zip_code="40100",
        city="Bologna",
        address="Via Python 3",
        country="IT",
        vat_id="IT123",
        fiscal_code="ABC123",
        sdi="ABC1234",
        pec="patrick@example.com",
    )
    graphql_client.force_login(user)

    with django_assert_num_queries(5):
        response = graphql_client.query(
            CURRENT_USER_QUERY,
            variables={"conference": conference.code},
        )

    assert "errors" not in response
    me = response["data"]["me"]
    calendar_url = me.pop("userScheduleFavouritesCalendarUrl")
    assert me == {
        "id": str(user.id),
        "name": "Patrick",
        "fullName": "Patrick Arminio",
        "email": user.email,
        "gender": "male",
        "dateBirth": "1990-01-01",
        "country": "IT",
        "openToRecruiting": True,
        "openToNewsletter": True,
        "canEditSchedule": True,
        "isPythonItaliaMember": False,
        "billingAddresses": [
            {
                "isBusiness": billing_address.is_business,
                "companyName": "Python Italia",
                "userGivenName": "Patrick",
                "userFamilyName": "Arminio",
                "zipCode": "40100",
                "city": "Bologna",
                "address": "Via Python 3",
                "country": "IT",
                "vatId": "IT123",
                "fiscalCode": "ABC123",
                "sdi": "ABC1234",
                "pec": "patrick@example.com",
            }
        ],
    }
    assert (
        f"/schedule/user-schedule-favourites-calendar/{conference.id}/{user.user_hashid()}?sig="
        in calendar_url
    )


@mark.django_db
def test_frontend_request_invitation_letter_page_query(
    graphql_client,
    django_assert_num_queries,
    mock_has_ticket,
    user,
):
    conference = ConferenceFactory()
    deadline = DeadlineFactory(
        conference=conference,
        type=Deadline.TYPES.invitation_letter_request,
    )
    invitation_letter_request = InvitationLetterRequestFactory(
        conference=conference,
        requester=user,
    )
    mock_has_ticket(conference, has_ticket=True, user=user)
    graphql_client.force_login(user)

    with django_assert_num_queries(6):
        response = graphql_client.query(
            REQUEST_INVITATION_LETTER_PAGE_QUERY,
            variables={"conference": conference.code},
        )

    assert "errors" not in response
    assert response["data"] == {
        "conference": {
            "id": str(conference.id),
            "invitationLetterRequestDeadline": {
                "id": str(deadline.id),
                "status": deadline.status.name,
                "start": deadline.start.isoformat(),
            },
        },
        "me": {
            "id": str(user.id),
            "hasAdmissionTicket": True,
            "invitationLetterRequest": {
                "id": str(invitation_letter_request.id),
                "status": "PENDING",
            },
        },
    }
