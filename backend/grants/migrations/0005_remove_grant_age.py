# Generated by Django 3.2.12 on 2022-12-08 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grants', '0004_grant_age_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grant',
            name='age',
        ),
    ]
