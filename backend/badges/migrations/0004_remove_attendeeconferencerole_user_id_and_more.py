# Generated by Django 4.2.3 on 2023-10-01 14:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("badges", "0003_alter_attendeeconferencerole_order_position_id_and_more"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.AlterField(
                    model_name="attendeeconferencerole",
                    name="user_id",
                    field=models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                        db_column="user_id",
                    ),
                ),
            ],
            state_operations=[
                migrations.RemoveField(
                    model_name="attendeeconferencerole",
                    name="user_id",
                ),
                migrations.AddField(
                    model_name="attendeeconferencerole",
                    name="user",
                    field=models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
        )
    ]
