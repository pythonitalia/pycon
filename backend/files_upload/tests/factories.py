import factory
from files_upload.models import File


class FileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = File

    file = factory.django.FileField(filename="test.txt", data=b"test data")
    uploaded_by = factory.SubFactory("users.tests.factories.UserFactory")
