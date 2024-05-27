from files_upload.tests.factories import FileFactory


def test_file_url():
    file = FileFactory()
    assert f"/files/participant_avatar/{file.id}.txt" in file.url
