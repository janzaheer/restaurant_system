# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-06 09:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_menu', '0003_auto_20180905_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
