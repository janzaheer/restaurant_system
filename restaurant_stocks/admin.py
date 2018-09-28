# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

from restaurant_stocks.models import (
    Stock, StockIn, StockOut,
    StockClosed, StockItemClosed
)


class StockAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'unit_type'
    )
    search_fields = ('item_name',)


class StockInAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'new_stock', 'price', 'total', 'created_at'
    )
    search_fields = (
        'stock__item_name',
    )


class StockOutAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'stock_out', 'created_at'
    )
    search_fields = (
        'stock__item_name',
    )


class StockClosedAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'closed_stock_in', 'closed_stock_out',
        'closed_stock_amount', 'remaining_stock'
    )
    list_filter = (('closing_date', DateFieldListFilter),)


class ClosedItemAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'stock_closed', 'item_stock_in', 'item_stock_out',
        'closed_stock_amount', 'remaining_stock_item'
    )
    search_fields = ('stock__item_name',)
    list_filter = (('stock_closed__closing_date', DateFieldListFilter),)
    raw_id_fields = ('stock', 'stock_closed',)


admin.site.register(Stock, StockAdmin)
admin.site.register(StockIn, StockInAdmin)
admin.site.register(StockOut, StockOutAdmin)
admin.site.register(StockClosed, StockClosedAdmin)
admin.site.register(StockItemClosed, ClosedItemAdmin)
