# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-24 09:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_sales', '0020_order_charges_percent'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paid',
            field=models.BooleanField(default=True),
        ),
    ]
