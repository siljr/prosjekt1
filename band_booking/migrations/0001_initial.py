# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-19 09:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('sales_numbers', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Band',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('band_name', models.CharField(max_length=30)),
                ('genre', models.CharField(max_length=20)),
                ('booking_price', models.IntegerField()),
                ('streaming_numbers', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_name', models.CharField(default=' ', max_length=50)),
                ('recipient_email', models.EmailField(default=' ', max_length=50)),
                ('email_text', models.CharField(default='Booking offer goes here', max_length=5000)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('U', 'Undecided'), ('N', 'Not approved'), ('A', 'Approved'), ('S', 'Sent')], default='U', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Concert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('concert_title', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('attendance', models.IntegerField(default=0)),
                ('ticket_price', models.IntegerField(default=0)),
                ('booking_price', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('B', 'Booked'), ('C', 'Contacted'), ('P', 'Paid')], max_length=1)),
                ('bands', models.ManyToManyField(to='band_booking.Band')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('telephone_number', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('role', models.CharField(choices=[('M', 'manager'), ('O', 'organizer'), ('R', 'rigger'), ('C', 'chief organizer'), ('V', 'volunteer')], default='V', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Scene',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_seats', models.IntegerField()),
                ('handicap_accessible', models.NullBooleanField()),
                ('expenditure', models.IntegerField(default=0)),
                ('scene_name', models.CharField(choices=[('Storsalen', 'storsalen'), ('Klubben', 'klubben'), ('Knaus', 'knaus'), ('Edgar', 'edgar')], default='Storsalen', max_length=16)),
            ],
        ),
        migrations.AddField(
            model_name='concert',
            name='personnel',
            field=models.ManyToManyField(to='band_booking.Person'),
        ),
        migrations.AddField(
            model_name='concert',
            name='scene',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='band_booking.Scene'),
        ),
        migrations.AddField(
            model_name='booking',
            name='scene',
            field=models.ForeignKey(blank=True, default=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='band_booking.Scene'),
        ),
        migrations.AddField(
            model_name='booking',
            name='sender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='band',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='band_booking.Person'),
        ),
        migrations.AddField(
            model_name='album',
            name='band',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='band_booking.Band'),
        ),
    ]
