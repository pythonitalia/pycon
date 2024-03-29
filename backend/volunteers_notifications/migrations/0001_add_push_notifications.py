# Generated by Django 3.2.12 on 2022-05-28 10:57

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.TextField()),
                ('subtitle', models.TextField(blank=True, default='')),
                ('body', models.TextField()),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='VolunteerDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('user_id', models.IntegerField(blank=True, null=True, verbose_name='user')),
                ('device_token', models.TextField(unique=True)),
                ('endpoint_arn', models.TextField(unique=True)),
                ('platform', models.CharField(choices=[('android', 'Android'), ('ios', 'iOS')], max_length=30)),
            ],
            options={
                'verbose_name': 'Volunteer Device',
                'verbose_name_plural': 'Volunteers Devices',
            },
        ),
    ]
