# Generated by Django 4.1.7 on 2023-05-13 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('badges', '0001_model_to_store_badge_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendeeconferencerole',
            name='roles',
            field=models.JSONField(default=list),
        ),
    ]
