# Generated by Django 3.2.12 on 2022-05-22 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0038_remove_old_speaker_voucher_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='type',
            field=models.CharField(choices=[('default', 'Default'), ('free_time', 'Free Time')], default='default', max_length=100, verbose_name='type'),
        ),
    ]
