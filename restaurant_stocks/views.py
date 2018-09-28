# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import (
    FormView, TemplateView, UpdateView, DeleteView, View
)
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Sum
from django.utils import timezone
from django.db import transaction

from restaurant_stocks.models import (
    Stock, StockIn, StockOut, StockClosed, StockItemClosed
)
from restaurant_stocks.forms import (
    StockForm, StockInForm, StockOutForm, ClosedStockForm, ClosedStockItemForm
)


class StockListView(TemplateView):
    template_name = 'stock/list.html'

    def get_context_data(self, **kwargs):
        context = super(StockListView, self).get_context_data(**kwargs)

        # Last Closed Stock Details
        try:
            last_closed_stock = StockClosed.objects.all().latest(
                'closing_date')
            last_stock_in = last_closed_stock.closed_stock_in
            last_stock_out = last_closed_stock.closed_stock_out
            last_stock_closed_amount = last_closed_stock.closed_stock_amount
            last_remaining_stock = last_closed_stock.remaining_stock
            last_closing_date = last_closed_stock.closing_date
        except:
            last_stock_in = 0
            last_stock_out = 0
            last_stock_closed_amount = 0
            last_remaining_stock = 0
            last_closing_date = 'Not Defined.'

        # Current Stock Details
        current_stock_in = StockIn.objects.filter(is_closed=False)
        if current_stock_in.exists():
            total_current_stock_in = current_stock_in.aggregate(
                Sum('new_stock'))
            total_current_stock_in = (
                total_current_stock_in.get('new_stock__sum') or 0)

            current_stock_amount = current_stock_in.aggregate(Sum('total'))
            current_stock_amount = current_stock_amount.get('total__sum') or 0
        else:
            total_current_stock_in = 0
            current_stock_amount = 0

        current_stock_out = StockOut.objects.filter(is_closed=False)
        if current_stock_out.exists():
            total_current_stock_out = current_stock_out.aggregate(
                Sum('stock_out'))
            total_current_stock_out = (
                total_current_stock_out.get('stock_out__sum') or 0)
        else:
            total_current_stock_out = 0

        # Overall Stock Details
        overall_stock_in = StockIn.objects.all()
        if overall_stock_in.exists():
            total_stock_in = overall_stock_in.aggregate(
                Sum('new_stock'))
            total_stock_in = total_stock_in.get('new_stock__sum') or 0

            total_stock_amount = overall_stock_in.aggregate(Sum('total'))
            total_stock_amount = total_stock_amount.get('total__sum') or 0
        else:
            total_stock_in = 0
            total_stock_amount = 0

        overall_stock_out = StockOut.objects.all()
        if overall_stock_out.exists():
            total_stock_out = overall_stock_out.aggregate(Sum('stock_out'))
            total_stock_out = total_stock_out.get('stock_out__sum') or 0
        else:
            total_stock_out = 0

        context.update({
            'stocks': Stock.objects.all().order_by('item_name'),
            'last_closing_date': last_closing_date,
            'last_stock_in': last_stock_in,
            'last_stock_out': last_stock_out,
            'last_stock_closed_amount': last_stock_closed_amount,
            'last_remaining_stock': last_remaining_stock,
            'current_stock_in': total_current_stock_in,
            'current_stock_out': total_current_stock_out,
            'current_stock_amount': current_stock_amount,
            'current_remaining_stock': (
                total_current_stock_in - total_current_stock_out),
            'total_stock_in': total_stock_in,
            'total_stock_out': total_stock_out,
            'total_stock_amount': total_stock_amount,
            'total_remaining_stock': total_stock_in - total_current_stock_out,
            'date': timezone.now().date(),
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

        # Current Stock Details
        item_stocks_in = stock.stock_stockin.filter(is_closed=False)
        if item_stocks_in.exists():
            current_stock_in = item_stocks_in.aggregate(Sum('new_stock'))
            current_stock_in = current_stock_in.get('new_stock__sum') or 0

            current_stock_amount = item_stocks_in.aggregate(Sum('total'))
            current_stock_amount = current_stock_amount.get('total__sum') or 0
        else:
            current_stock_in = 0
            current_stock_amount = 0

        item_stock_out = stock.stock_stockout.filter(is_closed=False)
        if item_stock_out.exists():
            current_stock_out = item_stock_out.aggregate(Sum('stock_out'))
            current_stock_out = current_stock_out.get('stock_out__sum') or 0
        else:
            current_stock_out = 0

        # Last Closed Stock Details
        try:
            last_closed_stock = StockItemClosed.objects.all().latest(
                'stock_closed__closing_date')
            context.update({
                'last_stock_in': (
                    last_closed_stock.item_stock_in or 0),
                'last_stock_out': (
                    last_closed_stock.item_stock_out or 0),
                'last_closing_date': (
                    last_closed_stock.stock_closed.closing_date or 0),
                'last_remaining_stock': (
                    last_closed_stock.remaining_stock_item or 0),
                'last_stock_amount': (
                    last_closed_stock.closed_stock_amount or 0)
            })
        except:
            context.update({
                'last_stock_in': 0,
                'last_stock_out': 0,
                'last_closing_date': 0,
                'last_remaining_stock': 0,
                'last_stock_amount': 0
            })

        context.update({
            'stock': stock,
            'stockin': stock.stock_stockin.all(),
            'stockout': stock.stock_stockout.all(),
            'current_stock_in': current_stock_in,
            'current_stock_out': current_stock_out,
            'current_stock_amount': current_stock_amount,
            'current_remaining_stock': current_stock_in - current_stock_out,
            'date': timezone.now().date(),
        })

        return context


class CloseStockView(View):
    def get(self, request, *args, **kwargs):

        stocks = Stock.objects.all()
        stock_in = StockIn.objects.filter(is_closed=False)

        if not stock_in.exists():
            return HttpResponseRedirect(reverse('stock_list'))

        try:
            previous_close_stock = StockClosed.objects.all().latest(
                'closing_date')
            previous_remaining_stock = (
                previous_close_stock.remaining_stock or 0)
        except:
            previous_remaining_stock = 0

        if stock_in.exists():
            total_closed_stock_in = stock_in.aggregate(Sum('new_stock'))
            total_closed_stock_in = (
                total_closed_stock_in.get('new_stock__sum') or 0)

            total_stock_amount = stock_in.aggregate(Sum('total'))
            total_stock_amount = (
                total_stock_amount.get('total__sum') or 0
            )
        else:
            total_closed_stock_in = 0
            total_stock_amount = 0

        stock_out = StockOut.objects.filter(is_closed=False)
        if stock_out.exists():
            total_closed_stock_out = stock_out.aggregate(Sum('stock_out'))
            total_closed_stock_out = (
                total_closed_stock_out.get('stock_out__sum') or 0)
        else:
            total_closed_stock_out = 0

        closing_date = timezone.now()

        closed_stock_form_kwargs = {
            'closed_stock_in': total_closed_stock_in,
            'closed_stock_out': total_closed_stock_out,
            'closing_date': closing_date,
            'closed_stock_amount': total_stock_amount,
            'remaining_stock': (
                total_closed_stock_in - total_closed_stock_out),
        }

        with transaction.atomic():
            closed_stock_form = ClosedStockForm(closed_stock_form_kwargs)
            if closed_stock_form.is_valid():
                closed_stock_obj = closed_stock_form.save()

                for stock in stocks:
                    try:
                        previous_remaining_item = StockItemClosed.objects.filter(
                            stock=stock).latest('close_stock__closing_date')
                        previous_remaining_item = (
                            previous_remaining_item.remaining_stock_item or 0)
                    except:
                        previous_remaining_item = 0
                    item_stocks_in = stock.stock_stockin.filter(is_closed=False)
                    if item_stocks_in.exists():
                        closed_item_stock_in = (
                            item_stocks_in.aggregate(Sum('new_stock')))
                        closed_item_stock_in = (
                            closed_item_stock_in.get('new_stock__sum') or 0)

                        closed_item_amount = item_stocks_in.aggregate(Sum('total'))
                        closed_item_amount = (
                            closed_item_amount.get('total__sum') or 0
                        )

                    else:
                        closed_item_stock_in = 0
                        closed_item_amount = 0

                    item_stocks_out = stock.stock_stockout.filter(is_closed=False)
                    if item_stocks_out:
                        closed_item_stock_out = (
                            item_stocks_out.aggregate(Sum('stock_out')))
                        closed_item_stock_out = (
                            closed_item_stock_out.get('stock_out__sum') or 0)
                    else:
                        closed_item_stock_out = 0

                    item_closed_form_kwargs = {
                        'item_stock_in': closed_item_stock_in,
                        'item_stock_out': closed_item_stock_out,
                        'closed_stock_amount': closed_item_amount,
                        'remaining_stock_item': (
                            closed_item_stock_in - closed_item_stock_out),
                        'stock_closed': closed_stock_obj.id,
                        'stock': stock.id,
                    }
                    item_closed_form = ClosedStockItemForm(
                        item_closed_form_kwargs)
                    if item_closed_form.is_valid():
                        item_closed_obj = item_closed_form.save()

                        if item_stocks_in.exists():
                            item_stocks_in.update(
                                closed_stock=item_closed_obj,
                                is_closed=True
                            )

                        if item_stocks_out.exists():
                            item_stocks_out.update(
                                is_closed=True
                            )

        return HttpResponseRedirect(reverse('stock_list'))


class StockClosedItemLogsView(TemplateView):
    template_name = 'stock/closed_item_logs.html'

    def get_context_data(self, **kwargs):
        context = super(
            StockClosedItemLogsView, self).get_context_data(**kwargs)

        try:
            stock = Stock.objects.get(id=self.kwargs.get('pk'))
        except Stock.DoesNotExist:
            return Http404(
                'Stock with the given id is not found in the database')

        closed_item_stocks = StockItemClosed.objects.filter(
            stock=stock).order_by('-stock_closed__closing_date')

        context.update({
            'closed_item_stocks': closed_item_stocks,
            'stock': stock
        })
        return context