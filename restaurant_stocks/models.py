# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Sum
from django.db import models

from common.models import DatedModel


class Stock(models.Model):
    UNIT_TYPE_KG = 'Kilogram'
    UNIT_TYPE_GRAM = 'Gram'
    UNIT_TYPE_LITRE = 'Litre'
    UNIT_TYPE_QUANTITY = 'Quantity'

    UNIT_TYPES = (
        (UNIT_TYPE_KG, 'Kilogram'),
        (UNIT_TYPE_GRAM, 'Gram'),
        (UNIT_TYPE_LITRE, 'Litre'),
        (UNIT_TYPE_QUANTITY, 'Quantity'),
    )

    item_name = models.CharField(max_length=200)
    unit_type = models.CharField(
        choices=UNIT_TYPES, default=UNIT_TYPE_KG,
        blank=True, null=True, max_length=200
    )

    def __unicode__(self):
        return self.item_name

    def remaining_stock(self):
        """
        Remaining Stock is the difference of  total sum of new_stock and
        total sum of stock_out
        :return:
        """
        stockin_sum = StockIn.objects.filter(
            stock=self)

        if stockin_sum.exists():
            stockin_sum = stockin_sum.aggregate(Sum('new_stock'))
            in_sum = stockin_sum.get('new_stock__sum') or 0
        else:
            in_sum = 0

        stockout_sum = StockOut.objects.filter(stock=self)

        if stockout_sum.exists():
            stockout_sum = stockout_sum.aggregate(Sum('stock_out'))
            out_sum = stockout_sum.get('stock_out__sum') or 0
        else:
            out_sum = 0

        return in_sum - out_sum

    def total_stock_in(self):
        stockin = self.stock_stockin.all()

        if stockin.exists():
            stockin = stockin.aggregate(Sum('new_stock'))
            total = stockin.get('new_stock__sum') or 0
        else:
            total = 0

        return total

    def total_stock_out(self):
        stockout = self.stock_stockout.all()

        if stockout.exists():
            stockout = stockout.aggregate(Sum('stock_out'))
            total = stockout.get('stock_out__sum') or 0
        else:
            total = 0

        return total

    def stock_total_price(self):
        stock_in_total = self.stock_stockin.all()
        if stock_in_total.exists():
            stock_in_total = stock_in_total.aggregate(Sum('total'))
            total_price = stock_in_total.get('total__sum') or 0
        else:
            total_price = 0

        return total_price


class StockIn(DatedModel):
    stock = models.ForeignKey(
        Stock, related_name='stock_stockin', blank=True, null=True
    )
    new_stock = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(
        max_digits=20, decimal_places=2, default=0, blank=True, null=True
    )
    total = models.DecimalField(
        max_digits=20, decimal_places=2, default=0, blank=True, null=True
    )

    def __unicode__(self):
        return self.stock.item_name


class StockOut(DatedModel):
    stock = models.ForeignKey(
        Stock, related_name='stock_stockout', blank=True, null=True
    )
    stock_out = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return self.stock.item_name
