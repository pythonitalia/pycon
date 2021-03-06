# Generated by Django 2.2.7 on 2019-11-30 09:13

from django.db import migrations
import i18n.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20190809_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=i18n.fields.I18nTextField(blank=True, verbose_name='content'),
        ),
        migrations.AlterField(
            model_name='post',
            name='excerpt',
            field=i18n.fields.I18nTextField(verbose_name='excerpt'),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=i18n.fields.I18nCharField(blank=True, max_length=200, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=i18n.fields.I18nCharField(max_length=200, verbose_name='title'),
        ),
    ]
