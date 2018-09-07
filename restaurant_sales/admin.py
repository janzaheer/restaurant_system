# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from restaurant_sales.models import Table, Order


class TableAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'table_name', 'table_type', 'created_at')

    search_fields = (
        'table_no', 'table_name', 'table_type'
    )


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'total_qty', 'sub_total', 'total_due', 'created_at'
    )
    filter_horizontal = ('items',)


admin.site.register(Table, TableAdmin)
admin.site.register(Order, OrderAdmin)
