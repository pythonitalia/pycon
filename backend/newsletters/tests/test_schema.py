from pytest import mark


@mark.django_db
def test_subscribe_to_newsletter(graphql_client):
    email = "me@example.it"
    variables = {"email": email}

    query = """
        mutation($email: String!) {
            subscribeToNewsletter(input: {
                email: $email
            }) {
            __typename

            ... on SubscribeToNewsletterErrors {
                validationEmail: email
            }

            ... on Subscription {
                id
                email
            }
        }
    }
    """
    resp = graphql_client.query(query, variables=variables)
    assert resp["data"]["subscribeToNewsletter"]["__typename"] == "Subscription"
    assert resp["data"]["subscribeToNewsletter"]["email"] == email


@mark.django_db
def test_unsubscribe_to_newsletter(graphql_client, subscription_factory):
    email = "me@example.it"

    subscription_factory.create(email=email)

    variables = {"email": email}

    query = """
            mutation($email: String!) {
                unsubscribeToNewsletter(input: {
                    email: $email
                }) {
                __typename

                ... on UnsubscribeToNewsletterErrors {
                    email
                }

                ... on OperationResult {
                    ok
                }
            }
        }
        """
    resp = graphql_client.query(query, variables=variables)
    assert resp["data"]["unsubscribeToNewsletter"]["__typename"] == "OperationResult"
    assert resp["data"]["unsubscribeToNewsletter"]["ok"] is True


@mark.django_db
def test_unsubscribe_not_registered_mail_to_newsletter(graphql_client):
    """If the mail is already unsubscribed (it's not in the subcription table)
    return true anyway"""

    email = "me@example.it"

    variables = {"email": email}

    query = """
            mutation($email: String!) {
                unsubscribeToNewsletter(input: {
                    email: $email
                }) {
                __typename

                ... on UnsubscribeToNewsletterErrors {
                    email
                }

                ... on OperationResult {
                    ok
                }
            }
        }
        """
    resp = graphql_client.query(query, variables=variables)
    assert resp["data"]["unsubscribeToNewsletter"]["__typename"] == "OperationResult"
    assert resp["data"]["unsubscribeToNewsletter"]["ok"] is True
