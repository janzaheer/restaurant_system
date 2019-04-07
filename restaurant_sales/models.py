# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random

from django.db import models
from django.db.models.signals import post_save
from common.models import DatedModel


class Table(DatedModel):
    table_no = models.IntegerField(verbose_name='Table No.', unique=True)
    table_name = models.CharField(max_length=100, blank=True, null=True)
    table_type = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return '%s' % self.table_no


class Order(DatedModel):
    table = models.ForeignKey(
        Table, related_name='order_table',
        null=True, blank=True, on_delete=models.SET_NULL
    )

    order_no = models.CharField(
        max_length=20, unique=True, blank=True, null=True
    )
    items = models.ManyToManyField(
        'restaurant_menu.PurchaseMenuItem', related_name='purchase_orders',
        max_length=100
    )
    total_qty = models.CharField(
        verbose_name='Total Quantity', blank=True,
        null=True, max_length=100
    )
    sub_total = models.DecimalField(
        max_digits=20, decimal_places=2, default=0, blank=True, null=True
    )
    discount = models.DecimalField(
        max_digits=20, decimal_places=2, default=0, blank=True, null=True
    )
    service_charges = models.DecimalField(
        max_digits=20, decimal_places=2, default=0, blank=True, null=True
    )
    charges_percent = models.DecimalField(
        max_digits=20, decimal_places=2, default=7, blank=True, null=True
    )
    total_due = models.DecimalField(
        max_digits=20, decimal_places=2, default=0, blank=True, null=True
    )
    paid = models.BooleanField(
        default=True
    )

    def __unicode__(self):
        return '%s' % self.order_no


# Signals Function
def create_save_order_no(sender, instance, created, **kwargs):
    if created and not instance.order_no:
        while True:
            random_code = random.randint(1000000, 9999999)
            if (
                not Order.objects.filter(
                    order_no=random_code).exists()
            ):
                break

        instance.order_no = random_code
        instance.save()


# Signal Calls
post_save.connect(create_save_order_no, sender=Order)
