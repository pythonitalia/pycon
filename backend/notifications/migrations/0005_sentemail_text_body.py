# Generated by Django 5.0.8 on 2024-08-25 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_alter_sentemail_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentemail',
            name='text_body',
            field=models.TextField(default='', verbose_name='text body'),
            preserve_default=False,
        ),
    ]
