# Generated by Django 4.2.7 on 2023-12-28 18:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("grants", "0013_remove_grant_travelling_from"),
    ]

    operations = [
        migrations.RenameField(
            model_name='grant',
            old_name='traveling_from',
            new_name='travelling_from',
        ),
    ]