# Generated by Django 4.2.7 on 2023-12-28 17:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("grants", "0012_grant_community_contribution_grant_github_handle_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="grant",
            name="travelling_from",
        ),
    ]