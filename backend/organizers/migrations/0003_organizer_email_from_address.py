# Generated by Django 5.0.8 on 2024-08-27 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizers', '0002_organizer_slack_oauth_bot_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizer',
            name='email_from_address',
            field=models.CharField(blank=True, default='', max_length=600, verbose_name='email from address'),
        ),
    ]
