# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import (
    FormView, TemplateView, UpdateView, DeleteView
)
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse, reverse_lazy

from restaurant_stocks.models import Stock
from restaurant_stocks.forms import StockForm, StockInForm, StockOutForm


class StockListView(TemplateView):
    template_name = 'stock/list.html'

    def get_context_data(self, **kwargs):
        context = super(StockListView, self).get_context_data(**kwargs)
        context.update({
            'stocks': Stock.objects.all().order_by('item_name')
        })
        return context


class StockFormView(FormView):
    form_class = StockForm
    template_name = 'stock/new_stock.html'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('stock_list'))


class StockInFormView(FormView):
    form_class = StockInForm
    template_name = 'stock/stock_in.html'

    def form_valid(self, form):
        stockin = form.save()
        return HttpResponseRedirect(
            reverse('stock_details', kwargs={'pk': stockin.stock.id})
        )

    def get_context_data(self, **kwargs):
        context = super(StockInFormView, self).get_context_data(**kwargs)
        try:
            stock = Stock.objects.get(id=self.kwargs.get('pk'))
        except Stock.DoesNotExist:
            return Http404('Stock Not Found in the Database')

        context.update({
            'stock': stock
        })
        return context


class StockOutFormView(FormView):
    form_class = StockOutForm
    template_name = 'stock/stock_out.html'

    def form_valid(self, form):
        stockout = form.save()
        return HttpResponseRedirect(
            reverse('stock_details', kwargs={'pk': stockout.stock.id})
        )

    def get_context_data(self, **kwargs):
        context = super(StockOutFormView, self).get_context_data(**kwargs)
        try:
            stock = Stock.objects.get(id=self.kwargs.get('pk'))
        except Stock.DoesNotExist:
            return Http404('Stock Not Found in the Database')

        context.update({
            'stock': stock
        })
        return context


class StockDetailView(TemplateView):
    template_name = 'stock/stock_details.html'

    def get_context_data(self, **kwargs):
        context = super(StockDetailView, self).get_context_data(**kwargs)
        try:
            stock = Stock.objects.get(id=self.kwargs.get('pk'))
        except Stock.DoesNotExist:
            return Http404('Stock does not found in the database')

        context.update({
            'stock': stock,
            'stockin': stock.stock_stockin.all(),
            'stockout': stock.stock_stockout.all()
        })

        return context
