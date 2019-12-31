# Generated by Django 2.2.8 on 2019-12-31 17:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import i18n.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conferences', '0017_auto_20191231_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotelRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', i18n.fields.I18nCharField(max_length=200, verbose_name='name')),
                ('description', i18n.fields.I18nTextField(blank=True, verbose_name='description')),
                ('total_capacity', models.PositiveIntegerField(verbose_name='total capacity')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='price')),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotel_rooms', to='conferences.Conference', verbose_name='conference')),
            ],
            options={
                'verbose_name': 'hotel room',
                'verbose_name_plural': 'hotel rooms',
            },
        ),
        migrations.CreateModel(
            name='HotelRoomReservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_code', models.CharField(max_length=200, verbose_name="pretix's order code")),
                ('checkin', models.DateField(verbose_name='checkin')),
                ('checkout', models.DateField(verbose_name='checkout')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='hotels.HotelRoom', verbose_name='room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'hotel room reservation',
                'verbose_name_plural': 'hotel room reservations',
            },
        ),
    ]
