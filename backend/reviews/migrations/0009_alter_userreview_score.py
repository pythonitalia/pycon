import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reviews", "0008_alter_reviewsession_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userreview",
            name="score",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="reviews.availablescoreoption",
            ),
        ),
    ]
