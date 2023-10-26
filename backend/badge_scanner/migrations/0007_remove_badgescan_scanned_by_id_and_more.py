# Generated by Django 4.2.3 on 2023-10-01 14:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("badge_scanner", "0006_rename_requested_by_badgescanexport_requested_by_id"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.AlterField(
                    model_name="badgescan",
                    name="scanned_by_id",
                    field=models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Scanned By",
                        db_column="scanned_by_id",
                    ),
                ),
                migrations.AlterField(
                    model_name="badgescan",
                    name="scanned_user_id",
                    field=models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Scanned User",
                        db_column="scanned_user_id",
                    ),
                ),
                migrations.AlterField(
                    model_name="badgescanexport",
                    name="requested_by_id",
                    field=models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Requested By",
                        db_column="requested_by_id",
                    ),
                ),
            ],
            state_operations=[
                migrations.RemoveField(
                    model_name="badgescan",
                    name="scanned_by_id",
                ),
                migrations.RemoveField(
                    model_name="badgescan",
                    name="scanned_user_id",
                ),
                migrations.RemoveField(
                    model_name="badgescanexport",
                    name="requested_by_id",
                ),
                migrations.AddField(
                    model_name="badgescan",
                    name="scanned_by",
                    field=models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Scanned By",
                    ),
                    preserve_default=False,
                ),
                migrations.AddField(
                    model_name="badgescan",
                    name="scanned_user",
                    field=models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Scanned User",
                    ),
                ),
                migrations.AddField(
                    model_name="badgescanexport",
                    name="requested_by",
                    field=models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Requested By",
                    ),
                    preserve_default=False,
                ),
            ],
        )
    ]