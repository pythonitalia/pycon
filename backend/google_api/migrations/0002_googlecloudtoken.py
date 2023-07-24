# Generated by Django 4.2.3 on 2023-07-22 11:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('google_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleCloudToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.TextField()),
                ('refresh_token', models.TextField()),
                ('token_uri', models.URLField()),
                ('client_id', models.TextField()),
                ('client_secret', models.TextField()),
                ('scopes', models.TextField()),
                ('admin_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('oauth_credential', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='google_api.googlecloudoauthcredential')),
            ],
        ),
    ]
