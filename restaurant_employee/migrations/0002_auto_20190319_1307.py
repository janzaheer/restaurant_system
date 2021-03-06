# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-03-19 08:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_employee', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeecreditrecord',
            name='credit_ammount',
        ),
        migrations.AddField(
            model_name='employeecreditrecord',
            name='credit_amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='employeecreditrecord',
            name='details',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='employeecreditrecord',
            name='date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
