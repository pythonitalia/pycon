# Generated by Django 5.0.8 on 2024-09-29 21:04

import i18n.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsors', '0023_alter_sponsorbenefit_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sponsorbenefit',
            name='value',
        ),
        migrations.RemoveField(
            model_name='sponsorlevelbenefit',
            name='value',
        ),
        migrations.AddField(
            model_name='sponsorlevelbenefit',
            name='value',
            field=i18n.fields.I18nCharField(default='✓', help_text='Value of the benefit, e.g. number of passes'),
        ),
    ]
