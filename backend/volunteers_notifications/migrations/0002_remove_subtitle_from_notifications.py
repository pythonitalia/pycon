# Generated by Django 3.2.12 on 2022-05-28 21:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers_notifications', '0001_add_push_notifications'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='subtitle',
        ),
    ]
