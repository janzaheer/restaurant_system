# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from common.models import DatedModel


class Category(DatedModel):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name


class Menu(DatedModel):
    category = models.ForeignKey(
        Category, related_name='category_menu',
        on_delete=models.SET_NULL, blank=True, null=True
    )
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(
        max_digits=20, decimal_places=2, default=0, blank=True, null=True
    )

    def __unicode__(self):
        return self.name


class PurchaseMenuItem(DatedModel):
    menu = models.ForeignKey(
        Menu, related_name='purchased_menu',
        on_delete=models.SET_NULL, blank=True, null=True
    )
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(
        max_digits=20, decimal_places=2, default=0, blank=True, null=True
    )
    total_price = models.DecimalField(
        max_digits=20, decimal_places=2, default=0, blank=True, null=True
    )

    def __unicode__(self):
        return self.menu.name

    def get_order_no(self):
        try:
            p_order = self.purchase_orders.get()
            return p_order.order_no
        except:
            return 0

    def get_bill_no(self):
        try:
            p_order = self.purchase_orders.get()
            return p_order.id
        except:
            return 0
