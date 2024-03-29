# Generated by Django 3.2.9 on 2021-12-30 15:58

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('conferences', '0018_new_grants_deadline'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keynote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('slug', models.SlugField(max_length=200, verbose_name='slug')),
                ('keynote_title', models.CharField(default='', max_length=512, verbose_name='keynote title')),
                ('keynote_description', models.TextField(default='', verbose_name='keynote description')),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='keynotes', to='conferences.conference', verbose_name='conference')),
            ],
            options={
                'verbose_name': 'Keynote',
                'verbose_name_plural': 'Keynotes',
                'ordering': ('order',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='KeynoteSpeaker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('name', models.CharField(max_length=512, verbose_name='fullname')),
                ('photo', models.ImageField(upload_to='keynotes', verbose_name='photo')),
                ('bio', models.TextField(verbose_name='bio')),
                ('pronouns', models.CharField(max_length=512, verbose_name='pronouns')),
                ('highlight_color', models.CharField(blank=True, choices=[('blue', 'blue'), ('yellow', 'yellow'), ('orange', 'orange'), ('cinderella', 'cinderella'), ('violet', 'violet'), ('green', 'green')], max_length=15, verbose_name='highlight color')),
                ('twitter_handle', models.CharField(blank=True, default='', max_length=1024, verbose_name='twitter handle')),
                ('instagram_handle', models.CharField(blank=True, default='', max_length=1024, verbose_name='instagram handle')),
                ('website', models.URLField(blank=True, default='', max_length=2049, verbose_name='website')),
                ('keynote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='speakers', to='conferences.keynote', verbose_name='keynote')),
            ],
            options={
                'verbose_name': 'Keynote Speaker',
                'verbose_name_plural': 'Keynote Speakers',
                'ordering': ('order',),
                'abstract': False,
            },
        ),
    ]
