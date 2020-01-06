from pytest import mark


def _submit_grant(client, conference, data):
    data = {"conference": conference.code, **data}

    return client.query(
        """mutation SendGrantRequest(
                $input: SendGrantRequestInput!
            ) {
                sendGrantRequest(input: $input) {
                    __typename

                    ... on GrantRequest {
                        id
                    }

                    ... on SendGrantRequestErrors {
                        validationConference: conference
                        validationEmail: email
                        validationName: name
                        validationFullName: fullName
                        validationGrantType: grantType
                        validationOccupation: occupation
                        validationOccupation: occupation
                        validationAge: age
                        validationPythonUsage: pythonUsage
                        validationBeenToOtherEvents: beenToOtherEvents
                        validationInterestedInVolunteering: interestedInVolunteering
                        validationNeedsFundsForTravel: needsFundsForTravel
                        validationWhy: why
                        validationNotes: notes
                        validationTravellingFrom: travellingFrom
                        nonFieldErrors
                    }
                }
            }""",
        variables={"input": data},
    )


@mark.django_db
def test_submit_grant(graphql_client, conference):
    resp = _submit_grant(
        graphql_client,
        conference,
        data={
            "name": "Patrick",
            "fullName": "Patrick A",
            "grantType": "speaker",
            "age": 1,
            "email": "patrick.arminio@gmail.com",
            "gender": "male",
            "occupation": "developer",
            "pythonUsage": "life",
            "beenToOtherEvents": "yes",
            "interestedInVolunteering": "yes",
            "needsFundsForTravel": False,
            "why": "this is a test",
            "notes": "this is a test",
            "travellingFrom": "london",
        },
    )

    assert not resp.get("errors")
    assert resp["data"]["sendGrantRequest"]["__typename"] == "GrantRequest"
