# Generated by Django 4.2.7 on 2024-01-10 16:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sponsors", "0009_sponsorlead_company"),
    ]

    operations = [
        migrations.AddField(
            model_name="sponsorlead",
            name="brochure_viewed",
            field=models.BooleanField(default=False),
        ),
    ]
