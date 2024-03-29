# Generated by Django 3.2.9 on 2022-01-01 14:35

from django.db import migrations
import i18n.fields
import json

def convert_data(apps, schema_editor):
    Keynote = apps.get_model("conferences", "Keynote")
    for keynote in Keynote.objects.all():
        keynote.slug = json.dumps({
            "en": keynote.slug
        })

        keynote.save()


class Migration(migrations.Migration):

    dependencies = [
        ('conferences', '0022_allow_multilanguage_keynote_info'),
    ]

    operations = [
        migrations.RunPython(convert_data),
        migrations.AlterField(
            model_name='keynote',
            name='slug',
            field=i18n.fields.I18nCharField(max_length=200, unique=True, verbose_name='slug'),
        ),
    ]
