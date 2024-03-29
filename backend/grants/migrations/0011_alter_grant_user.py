# Generated by Django 4.2.3 on 2023-10-08 23:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grants', '0010_remove_grant_user_id_grant_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grant',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
