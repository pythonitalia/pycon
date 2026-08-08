from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("video_uploads", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="WetransferToS3TransferRequest",
            new_name="VideosImportRequest",
        ),
        migrations.RenameField(
            model_name="videosimportrequest",
            old_name="wetransfer_url",
            new_name="source_url",
        ),
        migrations.AlterField(
            model_name="videosimportrequest",
            name="source_url",
            field=models.URLField(max_length=2048, verbose_name="Source URL"),
        ),
    ]
