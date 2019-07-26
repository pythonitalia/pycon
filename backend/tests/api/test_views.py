from django.urls import reverse


def test_graphql_as_get_renders_the_playground(http_client):
    response = http_client.get(reverse("graphql"))

    assert response.templates[0].name == "api/graphiql.html"


def test_graphql_only_post_and_get_are_allowed(http_client):
    response = http_client.patch(reverse("graphql"))

    assert response.status_code == 405
    assert response["allow"] == "GET, POST"
