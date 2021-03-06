# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-26 13:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_stocks', '0003_stockclosed_stockitemclosed'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockin',
            name='closed_stock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stock_in_closed', to='restaurant_stocks.StockItemClosed'),
        ),
    ]
