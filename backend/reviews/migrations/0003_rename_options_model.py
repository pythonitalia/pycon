# Generated by Django 4.1.6 on 2023-02-05 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_store_user_review'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AvailableVoteOption',
            new_name='AvailableScoreOption',
        ),
    ]
