# Generated by Django 5.1.4 on 2024-12-17 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visa', '0003_invitationletterattacheddocument_dynamic_document_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='InvitationLetterAttachedDocument',
            new_name='InvitationLetterDocument',
        ),
    ]
