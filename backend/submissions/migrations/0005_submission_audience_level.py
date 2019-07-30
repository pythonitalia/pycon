# Generated by Django 2.2.3 on 2019-07-29 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conferences', '0004_remove_conference_vote_range'),
        ('submissions', '0004_remove_submission_audience_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='audience_level',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='conferences.AudienceLevel', verbose_name='audience level'),
            preserve_default=False,
        ),
    ]
