# Generated by Django 5.1.4 on 2025-01-23 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0026_sync_pending_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubmissionConfirmPendingStatusProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Submission Confirm Pending Status',
                'verbose_name_plural': 'Submissions Confirm Pending Status',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('submissions.submission',),
        ),
    ]
