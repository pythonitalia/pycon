# Generated by Django 3.2.12 on 2022-11-19 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('participants', '0002_add_more_socials_to_participants'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='mastodon_handle',
            field=models.CharField(blank=True, max_length=2048),
        ),
    ]
