# Generated by Django 4.2.7 on 2024-06-22 00:23

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('files_upload', '0007_file_mime_type'),
        ('submissions', '0023_remove_submission_speaker_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProposalMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('url', models.URLField(blank=True, max_length=2049, null=True, verbose_name='url')),
                ('file', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='files_upload.file', verbose_name='file')),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='submissions.submission', verbose_name='proposal')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
