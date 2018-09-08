# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render

from django.views.generic import FormView, TemplateView, RedirectView
from django.http import HttpResponseRedirect
from django.db.models import Sum

from django.utils import timezone

from restaurant_sales.models import Order


class DashboardView(TemplateView):
    template_name = 'dashboard.html'


class ReportsView(TemplateView):
    template_name = 'reports.html'

    def get_context_data(self, **kwargs):
        context = super(ReportsView, self).get_context_data(**kwargs)
        total_order_amount = Order.objects.all()

        if total_order_amount:
            total_amount = total_order_amount.aggregate(Sum('total_due'))
            total_amount = float(total_amount.get('total_due__sum'))
        else:
            total_amount = 0

        todays_order_amount = Order.objects.filter(
            created_at__icontains=timezone.now().date()
        )

        if todays_order_amount:
            todays_amount = todays_order_amount.aggregate(Sum('total_due'))
            todays_amount = float(todays_amount.get('total_due__sum'))
        else:
            todays_amount = 0

        context.update({
            'total_order': Order.objects.all().count(),
            'total_order_amount': total_amount,
            'todays_order': todays_order_amount.count(),
            'todays_amount': todays_amount

        })
        return context