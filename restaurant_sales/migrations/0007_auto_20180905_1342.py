# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-05 08:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_sales', '0006_auto_20180905_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_qty',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Total Quantity'),
        ),
    ]
