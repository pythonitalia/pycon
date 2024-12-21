# Generated by Django 5.1.4 on 2024-12-21 03:18

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conferences', '0051_conference_location'),
        ('visa', '0008_alter_invitationletterasset_identifier'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='InvitationLetterOrganizerConfig',
            new_name='InvitationLetterConferenceConfig',
        ),
        migrations.AlterField(
            model_name='invitationletterasset',
            name='invitation_letter_organizer_config',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assets', to='visa.invitationletterconferenceconfig', verbose_name='invitation letter organizer config'),
        ),
        migrations.AlterField(
            model_name='invitationletterdocument',
            name='invitation_letter_organizer_config',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attached_documents', to='visa.invitationletterconferenceconfig', verbose_name='invitation letter organizer config'),
        ),
    ]
