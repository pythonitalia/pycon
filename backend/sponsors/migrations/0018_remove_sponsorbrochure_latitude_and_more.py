# Generated by Django 5.0.8 on 2024-09-29 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsors', '0017_alter_sponsorlevel_sponsors_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sponsorbrochure',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='sponsorbrochure',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='sponsorbrochure',
            name='map_link',
        ),
    ]
