# Generated by Django 5.0.8 on 2024-08-26 15:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conferences', '0045_conference_logo'),
        ('notifications', '0008_emailtemplate_is_system_template_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtemplate',
            name='conference',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='email_templates', to='conferences.conference', verbose_name='conference'),
        ),
    ]
