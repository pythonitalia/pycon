import datetime
from participants.tests.factories import ParticipantFactory
from files_upload.models import File
import time_machine
from files_upload.tasks import delete_unused_files
from files_upload.tests.factories import FileFactory
from django.utils import timezone


def test_delete_unused_files():
    file_1 = FileFactory(
        created=timezone.datetime(2010, 8, 10, 10, 0, 0, tzinfo=datetime.timezone.utc)
    )
    file_2 = FileFactory(
        created=timezone.datetime(2010, 10, 10, 5, 0, 0, tzinfo=datetime.timezone.utc)
    )

    file_3 = FileFactory(
        created=timezone.datetime(2010, 1, 4, 10, 0, 0, tzinfo=datetime.timezone.utc)
    )
    ParticipantFactory(photo_file=file_3)

    with time_machine.travel("2010-10-10 10:20:00Z", tick=False):
        delete_unused_files()

    assert not File.objects.filter(id=file_1.id).exists()
    assert File.objects.filter(id=file_2.id).exists()
    assert File.objects.filter(id=file_3.id).exists()
