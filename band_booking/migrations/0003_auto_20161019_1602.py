# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-19 14:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('band_booking', '0002_auto_20161019_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='band',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='concert',
            name='organizer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organizer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='concert',
            name='personnel',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
