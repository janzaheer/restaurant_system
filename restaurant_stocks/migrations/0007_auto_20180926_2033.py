# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-26 15:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_stocks', '0006_auto_20180926_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockin',
            name='closed_stock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stock_in_closed', to='restaurant_stocks.StockItemClosed'),
        ),
        migrations.AlterField(
            model_name='stockitemclosed',
            name='stock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stock_item_closed', to='restaurant_stocks.Stock'),
        ),
        migrations.AlterField(
            model_name='stockitemclosed',
            name='stock_closed',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stock_closed', to='restaurant_stocks.StockClosed'),
        ),
    ]
