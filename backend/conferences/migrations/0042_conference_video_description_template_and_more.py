# Generated by Django 4.2.7 on 2024-03-03 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conferences', '0041_remove_conference_visa_application_form_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='video_description_template',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='conference',
            name='video_title_template',
            field=models.TextField(blank=True, default=''),
        ),
    ]
