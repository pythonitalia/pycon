# Generated by Django 2.2.8 on 2020-03-22 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0011_submission_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='submissiontype',
            name='allow_booking',
            field=models.BooleanField(default=False, verbose_name='allow booking'),
        ),
    ]
