# Generated by Django 4.2.7 on 2024-05-19 18:29

from django.db import migrations, models
import files_upload.models


class Migration(migrations.Migration):

    dependencies = [
        ('files_upload', '0002_alter_file_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=files_upload.models.get_upload_to_from_instance, verbose_name='File'),
        ),
    ]