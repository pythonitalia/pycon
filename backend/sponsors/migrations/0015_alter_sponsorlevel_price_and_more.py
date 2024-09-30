# Generated by Django 5.0.8 on 2024-09-30 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsors', '0014_delete_sponsorbrochure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsorlevel',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='sponsorspecialoption',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='price'),
        ),
    ]
