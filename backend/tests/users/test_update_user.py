import datetime

from pytest import mark

from users.models import User


def _update_user(graphql_client, user, **kwargs):

    defaults = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "gender": user.gender,
        "open_to_recruiting": user.open_to_recruiting,
        "date_birth": f"{user.date_birth:%Y-%m-%d}" if user.date_birth else "",
        "business_name": user.business_name,
        "fiscal_code": user.fiscal_code,
        "vat_number": user.vat_number,
        "phone_number": user.phone_number,
        "recipient_code": user.recipient_code,
        "pec_address": user.pec_address,
        "address": user.address,
        "country": user.country if user.country else "",
    }
    variables = {**defaults, **kwargs}

    query = """
    mutation(
        $first_name: String,
        $last_name: String,
        $gender: String,
        $open_to_recruiting: Boolean!,
        $date_birth: String,
        $business_name: String,
        $fiscal_code: String,
        $vat_number: String,
        $phone_number: String,
        $recipient_code: String,
        $pec_address: String,
        $address: String,
        $country: String
    ){
        update(input: {
            firstName: $first_name,
            lastName: $last_name,
            gender: $gender,
            openToRecruiting: $open_to_recruiting,
            dateBirth: $date_birth,
            businessName: $business_name,
            fiscalCode: $fiscal_code,
            vatNumber: $vat_number,
            phoneNumber: $phone_number,
            recipientCode: $recipient_code,
            pecAddress: $pec_address,
            address: $address,
            country: $country
        }){
            __typename
            ... on MeUserType {
                id
                firstName
                lastName
                gender
                openToRecruiting
                dateBirth
                businessName
                fiscalCode
                vatNumber
                phoneNumber
                recipientCode
                pecAddress
                address
                country
            }
            ... on UpdateErrors {
                validationFirstName: firstName
                validationLastName: lastName
                validationGender: gender
                validationOpenToRecruiting: openToRecruiting
                validationDateBirth: dateBirth
                validationBusinessName: businessName
                validationFiscalCode: fiscalCode
                validationVatNumber: vatNumber
                validationPhoneNumber: phoneNumber
                validationRecipientCode: recipientCode
                validationPecAddress: pecAddress
                validationAddress: address
                validationCountry: country
                nonFieldErrors
            }
        }
    }
    """
    return (graphql_client.query(query=query, variables=variables), variables)


@mark.django_db
def test_update(graphql_client, user_factory):
    user = user_factory(
        first_name="John",
        last_name="Lennon",
        gender="male",
        open_to_recruiting=True,
        date_birth=datetime.datetime.strptime("1940-10-09", "%Y-%m-%d"),
        address="P Sherman, 42 Wallaby Way, Sydney",
        country="AT",
        business_name="John Lennon Ltd",
        fiscal_code="LNNJHN40R09H501E",
        vat_number="IT12345678901",
        phone_number="+39 3381234567",
        recipient_code="1234567",
        pec_address="lennon@pec.it",
    )
    graphql_client.force_login(user)
    resp, variables = _update_user(graphql_client, user)

    assert resp["data"]["update"]["__typename"] == "MeUserType"
    assert resp["data"]["update"]["id"] == str(user.id)
    assert resp["data"]["update"]["firstName"] == variables["first_name"]
    assert resp["data"]["update"]["lastName"] == variables["last_name"]
    assert resp["data"]["update"]["dateBirth"] == variables["date_birth"]
    assert resp["data"]["update"]["address"] == variables["address"]
    assert resp["data"]["update"]["country"] == variables["country"]
    assert resp["data"]["update"]["businessName"] == variables["business_name"]
    assert resp["data"]["update"]["fiscalCode"] == variables["fiscal_code"]
    assert resp["data"]["update"]["vatNumber"] == variables["vat_number"]
    assert resp["data"]["update"]["phoneNumber"] == variables["phone_number"]
    assert resp["data"]["update"]["recipientCode"] == variables["recipient_code"]
    assert resp["data"]["update"]["pecAddress"] == variables["pec_address"]


@mark.django_db
def test_update_not_authenticated_user_error(graphql_client):
    user, _ = User.objects.get_or_create(email="user@example.it", password="password")
    resp, variables = _update_user(graphql_client, user)

    assert resp["data"]["update"]["__typename"] == "UpdateErrors"
    assert resp["data"]["update"]["nonFieldErrors"] == [
        "Must authenticate to update User information"
    ]
