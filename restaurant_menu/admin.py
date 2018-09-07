# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from restaurant_menu.models import Menu, Category, PurchaseMenuItem


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'created_at', 'updated_at')
    search_fields = ('name',)


class MenuAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'category', 'price', 'created_at')
    search_fields = ('name', 'category__name',)
    raw_id_fields = ('category',)


class PurchasedMenuAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'order', 'quantity', 'total_price', 'created_at')
    search_fields = ('menu__name', 'menu__category__name')
    raw_id_fields = ('menu',)

    @staticmethod
    def order(obj):
        try:
            p_order = obj.purchase_orders.get()
            return p_order.order_no
        except:
            return 0


admin.site.register(Category, CategoryAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(PurchaseMenuItem, PurchasedMenuAdmin)
