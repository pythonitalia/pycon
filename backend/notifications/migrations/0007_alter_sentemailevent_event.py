# Generated by Django 5.0.8 on 2024-08-26 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0006_sentemail_from_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentemailevent',
            name='event',
            field=models.CharField(choices=[('bounced', 'Bounced'), ('delivered', 'Delivered'), ('opened', 'Opened'), ('clicked', 'Clicked'), ('complaint', 'Complaint'), ('unsubscribed', 'Unsubscribed'), ('rejected', 'Rejected'), ('sent', 'Sent')], max_length=200, verbose_name='event'),
        ),
    ]
