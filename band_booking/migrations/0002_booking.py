# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-03 14:53

from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('band_booking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_name', models.CharField(default=' ', max_length=50)),
                ('recipient_email', models.EmailField(default=' ', max_length=50)),
                ('email_text', models.CharField(default='Booking offer goes here', max_length=5000)),
                ('status', models.CharField(choices=[('U', 'Undecided'), ('N', 'Not approved'), ('A', 'Approved'), ('S', 'Sent')], default='U', max_length=1)),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
