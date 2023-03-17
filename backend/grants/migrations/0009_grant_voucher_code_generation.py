# Generated by Django 4.1.7 on 2023-03-17 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grants', '0008_alter_grant_traveling_from'),
    ]

    operations = [
        migrations.AddField(
            model_name='grant',
            name='pretix_voucher_id',
            field=models.IntegerField(blank=True, help_text='ID of the voucher in the Pretix database', null=True),
        ),
        migrations.AddField(
            model_name='grant',
            name='voucher_code',
            field=models.TextField(blank=True, help_text='Voucher code generated for this grant.', null=True),
        ),
        migrations.AddField(
            model_name='grant',
            name='voucher_email_sent_at',
            field=models.DateTimeField(blank=True, help_text='When the email was last sent', null=True),
        ),
    ]
