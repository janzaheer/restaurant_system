# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from restaurant_stocks.models import Stock, StockIn, StockOut


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


admin.site.register(Stock, StockAdmin)
admin.site.register(StockIn, StockInAdmin)
admin.site.register(StockOut, StockOutAdmin)
