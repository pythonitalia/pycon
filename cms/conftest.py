import os
from api.tests.factories import *  # noqa
from sites.tests.factories import *  # noqa
from news.tests.factories import *  # noqa

import pytest
from wagtail.models import Locale
from strawberry.django.test.client import GraphQLTestClient
from io import BytesIO

import PIL.Image
from django.core.files.images import ImageFile
from django.contrib.auth import get_user_model


@pytest.fixture
def create_user():
    return lambda **kwargs: get_user_model().objects.create_user(**kwargs)


@pytest.fixture
def locale():
    return lambda code: Locale.objects.get_or_create(language_code=code)[0]


@pytest.fixture
def graphql_client(client):
    return GraphQLTestClient(client=client)


@pytest.fixture
def image_file():
    def wrapper(filename: str = "test.jpg"):
        file = BytesIO()
        image = PIL.Image.new("RGB", (640, 480), "white")
        image.save(file, "JPEG")

        yield ImageFile(file, name=filename)

        os.remove(filename)

    return wrapper
