def _scan_badge_mutation(graphql_client, variables):
    return graphql_client.query(
        """
        mutation ScanBadge($url: String!) {
            scanBadge(input: { url: $url }) {
                __typename
                ... on ScanSuccess {
                    badgeScan {
                        attendee {
                            fullName
                            email
                        }
                        notes
                    }
                }
                ... on ScanError {
                    message
                }
            }
        }
        """,
        variables=variables,
    )


def test_raises_an_error_when_user_is_not_authenticated(graphql_client):
    resp = _scan_badge_mutation(graphql_client, variables={"url": "https://foo.bar"})

    assert resp["errors"]
    assert resp["errors"][0]["message"] == "User not logged in"


# def test_works_when_user_is_logged_in(user, graphql_client):
#     graphql_client.force_login(user)

#     resp = graphql_client.query(
#         """
#         {
#             me {
#                 email
#             }
#         }
#         """
#     )

#     assert "errors" not in resp
#     assert resp["data"]["me"]["email"] == user.email


# @pytest.mark.django_db
# def test_query_submissions(graphql_client, user, submission_factory):
#     graphql_client.force_login(user)

#     submission = submission_factory(speaker_id=user.id)

#     response = graphql_client.query(
#         """query Submissions($conference: String!) {
#             me {
#                 submissions(conference: $conference) {
#                     id
#                 }
#             }
#         }""",
#         variables={"conference": submission.conference.code},
#     )

#     assert "errors" not in response
#     assert len(response["data"]["me"]["submissions"]) == 1
#     assert response["data"]["me"]["submissions"][0]["id"] == submission.hashid


# def test_can_edit_schedule(user, graphql_client):
#     graphql_client.force_login(user)

#     resp = graphql_client.query(
#         """
#         {
#             me {
#                 canEditSchedule
#             }
#         }
#         """
#     )

#     assert "errors" not in resp
#     assert resp["data"]["me"]["canEditSchedule"] is False
