# Generated by Django 5.0.8 on 2024-08-17 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizer',
            name='slack_oauth_bot_token',
            field=models.CharField(blank=True, default='', help_text='Slack OAuth bot token', max_length=255),
        ),
    ]
