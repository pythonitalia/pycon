# Generated by Django 5.0.8 on 2024-08-24 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtemplate',
            name='identifier',
            field=models.CharField(choices=[('proposal_accepted', 'Proposal accepted'), ('proposal_rejected', 'Proposal rejected'), ('proposal_in_waiting_list', 'Proposal in waiting list'), ('proposal_scheduled_time_changed', 'Proposal scheduled time changed'), ('voucher_code', 'Voucher code'), ('custom', 'Custom')], max_length=200, verbose_name='identifier'),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='reply_to',
            field=models.EmailField(blank=True, default='', max_length=254, verbose_name='reply to'),
            preserve_default=False,
        ),
    ]