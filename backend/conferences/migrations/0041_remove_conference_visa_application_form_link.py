# Generated by Django 4.2.7 on 2024-02-13 13:46

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("conferences", "0040_conference_visa_application_form_link"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="conference",
            name="visa_application_form_link",
        ),
    ]
