# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-05 09:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_menu', '0003_auto_20180905_1253'),
        ('restaurant_sales', '0007_auto_20180905_1342'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('order_no', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('total_qty', models.CharField(blank=True, max_length=100, null=True, verbose_name='Total Quantity')),
                ('sub_total', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True)),
                ('total_due', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True)),
                ('items', models.ManyToManyField(max_length=100, related_name='purchase_orders2', to='restaurant_menu.PurchaseMenuItem')),
                ('table', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order2_table', to='restaurant_sales.Table')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(max_length=100, related_name='purchase_orders', to='restaurant_menu.PurchaseMenuItem'),
        ),
    ]
