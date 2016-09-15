# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-15 14:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mypage', '0012_concert_scene'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='concert',
            name='scene',
        ),
        migrations.AddField(
            model_name='concert',
            name='band',
            field=models.OneToOneField(default='Odd', on_delete=django.db.models.deletion.CASCADE, to='mypage.Band'),
        ),
    ]
