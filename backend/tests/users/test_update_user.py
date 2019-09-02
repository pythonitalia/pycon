import datetime
import json
import os

import pytest
from PIL import Image

from django.test import RequestFactory, override_settings
from upload.views import file_upload
from users.models import User


def _update_user(graphql_client, user, **kwargs):

    defaults = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "gender": user.gender,
        "open_to_recruiting": user.open_to_recruiting,
        "open_to_newsletter": user.open_to_newsletter,
        "date_birth": f"{user.date_birth:%Y-%m-%d}" if user.date_birth else "",
        "country": user.country if user.country else "",
    }
    variables = {**defaults, **kwargs}

    query = """
    mutation(
        $first_name: String,
        $last_name: String,
        $gender: String,
        $open_to_recruiting: Boolean!,
        $open_to_newsletter: Boolean!,
        $date_birth: String,
        $country: String
    ){
        update(input: {
            firstName: $first_name,
            lastName: $last_name,
            gender: $gender,
            openToRecruiting: $open_to_recruiting,
            openToNewsletter: $open_to_newsletter,
            dateBirth: $date_birth,
            country: $country
        }){
            __typename
            ... on MeUserType {
                id
                firstName
                lastName
                gender
                openToRecruiting
                openToNewsletter
                dateBirth
                country
            }
            ... on UpdateErrors {
                validationFirstName: firstName
                validationLastName: lastName
                validationGender: gender
                validationOpenToRecruiting: openToRecruiting
                validationOpenToNewsletter: openToNewsletter
                validationDateBirth: dateBirth
                validationCountry: country
                nonFieldErrors
            }
        }
    }
    """
    return (graphql_client.query(query=query, variables=variables), variables)


def _update_image(graphql_client, user, image):

    variables = {"user": user.id, "url": image}

    query = """
        mutation(
            $url: String!
        ){
            updateImage(input: {url: $url}) {
                __typename
                ... on UpdateImageErrors {
                    validationUrl: url
                    nonFieldErrors
                }
                ... on MeUserType {
                    id
                    image {
                        url
                    }
                }
            }
        }
    """
    return (graphql_client.query(query=query, variables=variables), variables)


def _upload_image(path):
    post_data = {"file": open(path, "rb")}
    request = RequestFactory().post("upload/", data=post_data)
    resp = file_upload(request)
    return json.loads(resp.content)["url"]


@pytest.fixture()
def create_sample_image():

    img = Image.new("RGB", (60, 30), color="red")
    path = "sample.png"
    img.save(path)

    yield (img, _upload_image(path))

    if os.path.exists(path):
        return os.remove(path)


@pytest.mark.django_db
def test_update(graphql_client, user_factory):
    user = user_factory(
        first_name="John",
        last_name="Lennon",
        gender="male",
        open_to_recruiting=True,
        open_to_newsletter=True,
        date_birth=datetime.datetime.strptime("1940-10-09", "%Y-%m-%d"),
        country="AT",
    )
    graphql_client.force_login(user)
    resp, variables = _update_user(graphql_client, user)

    assert resp["data"]["update"]["__typename"] == "MeUserType"
    assert resp["data"]["update"]["id"] == str(user.id)
    assert resp["data"]["update"]["firstName"] == variables["first_name"]
    assert resp["data"]["update"]["lastName"] == variables["last_name"]
    assert resp["data"]["update"]["gender"] == variables["gender"]
    assert resp["data"]["update"]["openToRecruiting"] == variables["open_to_recruiting"]
    assert resp["data"]["update"]["openToNewsletter"] == variables["open_to_newsletter"]
    assert resp["data"]["update"]["dateBirth"] == variables["date_birth"]
    assert resp["data"]["update"]["country"] == variables["country"]


@pytest.mark.django_db
@override_settings(MEDIA_ROOT="/tmp/django_test")
def test_update_image(graphql_client, create_sample_image):
    img, path = create_sample_image

    user, _ = User.objects.get_or_create(email="user@example.it", password="password")
    graphql_client.force_login(user)

    resp, variables = _update_image(graphql_client, user, path)

    assert resp["data"]["updateImage"]["__typename"] == "MeUserType"
    assert (
        os.path.basename(variables["url"])
        in resp["data"]["updateImage"]["image"]["url"]
    )


@pytest.mark.django_db
def test_update_image_file_not_fount(graphql_client):
    user, _ = User.objects.get_or_create(email="user@example.it", password="password")
    graphql_client.force_login(user)

    resp, variables = _update_image(graphql_client, user, "boh/file_not_found.jpg")

    assert resp["data"]["updateImage"]["__typename"] == "UpdateImageErrors"
    assert resp["data"]["updateImage"]["validationUrl"] == [
        "File 'file_not_found.jpg' not found"
    ]
