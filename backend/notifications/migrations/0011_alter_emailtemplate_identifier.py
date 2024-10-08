# Generated by Django 5.0.8 on 2024-08-26 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0010_alter_emailtemplate_identifier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtemplate',
            name='identifier',
            field=models.CharField(choices=[('proposal_accepted', 'Proposal accepted'), ('proposal_rejected', 'Proposal rejected'), ('proposal_in_waiting_list', 'Proposal in waiting list'), ('proposal_scheduled_time_changed', 'Proposal scheduled time changed'), ('voucher_code', 'Voucher code'), ('reset_password', '[System] Reset password'), ('custom', 'Custom')], max_length=200, verbose_name='identifier'),
        ),
    ]
