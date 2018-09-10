# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from calendar import monthrange
from django.views.generic import View
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Sum

from django.utils import timezone

from dateutil.relativedelta import relativedelta

from restaurant_sales.models import Order
from restaurant_stocks.models import Stock, StockIn, StockOut


class DailyOrdersAPIView(View):

    @staticmethod
    def get_data(obj_set, date):
        if obj_set.exists():
            total = obj_set.aggregate(Sum('total_due'))
            total = total.get('total_due__sum') or 0
        else:
            total = 0

        return {
            'total_price': total,
            'date': date.strftime('%m/%d/%Y')
        }

    def get(self, request, *args, **kwargs):
        orders = []
        for day in range(12):
            orders_day = timezone.now() - relativedelta(days=day)

            orders_set = Order.objects.filter(
                created_at__year=orders_day.year,
                created_at__month=orders_day.month,
                created_at__day=orders_day.day
            )
            data = self.get_data(obj_set=orders_set, date=orders_day.date())
            orders.append(data)

        return JsonResponse({
            'orders': orders
        })


class DailyOrdersListAPIView(DailyOrdersAPIView):
    def get(self, request, *args, **kwargs):
        orders = []
        for day in range(12):
            orders_day = timezone.now() - relativedelta(days=day)

            orders_set = Order.objects.filter(
                created_at__year=orders_day.year,
                created_at__month=orders_day.month,
                created_at__day=orders_day.day
            )
            data = self.get_data(obj_set=orders_set, date=orders_day.date())
            orders.append(data)

        return JsonResponse({
            'orders': orders
        })


class MonthlyOrderAPIView(View):

    @staticmethod
    def get_data(obj_set, date):
        if obj_set.exists():
            total = obj_set.aggregate(Sum('total_due'))
            total = total.get('total_due__sum') or 0
        else:
            total = 0

        return {
            'total_price': total,
            'date': date.strftime('%b %Y')
        }

    def get(self, request, *args, **kwargs):
        orders = []
        for month in range(12):
            orders_month = timezone.now() - relativedelta(months=month)
            month_range = monthrange(orders_month.year, orders_month.month)

            start_month = datetime.datetime(
                orders_month.year, orders_month.month, 1)

            end_month = datetime.datetime(
                orders_month.year, orders_month.month, month_range[1]
            )

            orders_set = Order.objects.filter(
                created_at__gt=start_month,
                created_at__lt=end_month.replace(
                    hour=23, minute=59, second=59),
            )
            data = self.get_data(obj_set=orders_set, date=start_month)
            orders.append(data)

        return JsonResponse({
            'orders': orders
        })


class DailyStocksAPIView(View):
    @staticmethod
    def get_data(in_set, out_set, date):
        if in_set.exists():
            total_in = in_set.aggregate(Sum('new_stock'))
            total_in = total_in.get('new_stock__sum') or 0
        else:
            total_in = 0

        if out_set.exists():
            total_out = out_set.aggregate(Sum('stock_out'))
            total_out = total_out.get('stock_out__sum') or 0
        else:
            total_out = 0

        return {
            'total_stock_in': total_in,
            'total_stock_out': total_out,
            'date': date.strftime('%m/%d/%Y')
        }

    def get(self, request, *args, **kwargs):
        stocks = []
        for day in range(12):
            stocks_day = timezone.now() - relativedelta(days=day)
            stock_in_set = StockIn.objects.filter(
                created_at__year=stocks_day.year,
                created_at__month=stocks_day.month,
                created_at__day=stocks_day.day
            )
            stock_out_set = StockOut.objects.filter(
                created_at__year=stocks_day.year,
                created_at__month=stocks_day.month,
                created_at__day=stocks_day.day
            )
            data = self.get_data(
                in_set=stock_in_set, out_set=stock_out_set,
                date=stocks_day.date()
            )
            stocks.append(data)

        return JsonResponse({
            'stocks': stocks
        })


class MonthlyStocksAPIView(View):
    @staticmethod
    def get_data(in_set, out_set, date):
        if in_set.exists():
            total_in = in_set.aggregate(Sum('new_stock'))
            total_in = total_in.get('new_stock__sum') or 0
        else:
            total_in = 0

        if out_set.exists():
            total_out = out_set.aggregate(Sum('stock_out'))
            total_out = total_out.get('stock_out__sum') or 0
        else:
            total_out = 0

        return {
            'total_stock_in': total_in,
            'total_stock_out': total_out,
            'date': date.strftime('%b %Y')
        }

    def get(self, request, *args, **kwargs):
        stocks = []
        for month in range(12):
            orders_month = timezone.now() - relativedelta(months=month)
            month_range = monthrange(orders_month.year, orders_month.month)

            start_month = datetime.datetime(
                orders_month.year, orders_month.month, 1)

            end_month = datetime.datetime(
                orders_month.year, orders_month.month, month_range[1]
            )
            stock_in_set = StockIn.objects.filter(
                created_at__gt=start_month,
                created_at__lt=end_month.replace(
                    hour=23, minute=59, second=59),
            )

            stock_out_set = StockOut.objects.filter(
                created_at__gt=start_month,
                created_at__lt=end_month.replace(
                    hour=23, minute=59, second=59),
            )
            data = self.get_data(
                in_set=stock_in_set, out_set=stock_out_set, date=start_month
            )
            stocks.append(data)

        return JsonResponse({
            'stocks': stocks
        })
