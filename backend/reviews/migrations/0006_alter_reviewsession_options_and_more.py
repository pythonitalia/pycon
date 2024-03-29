# Generated by Django 4.2.7 on 2024-01-14 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("reviews", "0005_reviewsession_status"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="reviewsession",
            options={"permissions": [("can_review", "Can review")]},
        ),
        migrations.AlterField(
            model_name="userreview",
            name="review_session",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_reviews",
                to="reviews.reviewsession",
            ),
        ),
    ]
