# Generated by Django 5.1.4 on 2025-01-05 22:09

from django.db import migrations


def migrate_data(apps, schema_editor):
    InvitationLetterDocument = apps.get_model('visa', 'InvitationLetterDocument')
    for document in InvitationLetterDocument.objects.all():
        if document.dynamic_document:
            dynamic_doc = document.dynamic_document
            dynamic_doc['page_layout'] = {
                'margin': '1cm 0 1cm 0'
            }
            dynamic_doc['header'] = {
                'content': dynamic_doc['header'],
                'align': 'top-left',
                'margin': '1cm 0 0 0'
            }
            dynamic_doc['footer'] = {
                'content': dynamic_doc['footer'],
                'align': 'bottom-left',
                'margin': '0 0 1cm 0'
            }
            document.dynamic_document = dynamic_doc
            document.save()


class Migration(migrations.Migration):

    dependencies = [
        ('visa', '0002_invitationletterdocument_inclusion_policy'),
    ]

    operations = [
        migrations.RunPython(migrate_data, reverse_code=migrations.RunPython.noop),
    ]
