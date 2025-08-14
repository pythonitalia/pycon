# Generated manually to change conference name from I18nCharField to CharField

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conferences', '0054_conference_frontend_revalidate_secret_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conference',
            name='name',
            field=models.CharField(max_length=100, verbose_name='name'),
        ),
    ]