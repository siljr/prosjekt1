# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-15 13:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypage', '0004_auto_20160915_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='concert',
            name='date',
            field=models.DateField(default=datetime.date(2016, 9, 15), verbose_name='Date'),
        ),
    ]
