# Generated by Django 4.2.7 on 2024-05-02 19:06

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('conferences', '0042_conference_video_description_template_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailSpeaker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('subject', models.CharField(max_length=988)),
                ('body', models.TextField()),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='email_speakers', to='conferences.conference', verbose_name='conference')),
            ],
            options={
                'verbose_name_plural': 'Emails to speakers',
            },
        ),
    ]
