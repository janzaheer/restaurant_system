# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.views.generic import (
    FormView, TemplateView, View, UpdateView, DeleteView
)
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from restaurant_menu.models import Menu, PurchaseMenuItem
from restaurant_sales.models import Table, Order
from restaurant_menu.forms import PurchasedMenuItemForm
from restaurant_sales.forms import TableForm, OrderForm

from django.core.urlresolvers import reverse, reverse_lazy
from django.utils import timezone


class TableListView(TemplateView):
    template_name = 'table/list.html'

    def get_context_data(self, **kwargs):
        context = super(TableListView, self).get_context_data(**kwargs)
        context.update({
            'tables': Table.objects.all().order_by('created_at')
        })
        return context


class TableFormView(FormView):
    template_name = 'table/add.html'
    form_class = TableForm
    success_url = reverse_lazy('table_list')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('table_list'))

    def form_invalid(self, form):
        return super(TableFormView, self).form_invalid(form)


class TableUpdateView(UpdateView):
    template_name = 'table/update.html'
    form_class = TableForm
    success_url = reverse_lazy('table_list')
    model = Table


class TableDeleteView(DeleteView):
    model = Table
    success_url = reverse_lazy('table_list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class OrderListView(TemplateView):
    template_name = 'order/list.html'

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        context.update({
            'orders': Order.objects.all().order_by('-created_at')
        })
        return context


class OrderCreateView(TemplateView):
    template_name = 'order/create.html'

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        context.update({
            'timezone': timezone.now(),
            'tables': Table.objects.all().order_by('table_no')
        })
        return context


class OrderUpdateView(TemplateView):
    template_name = 'order/update.html'

    def get_context_data(self, **kwargs):
        context = super(OrderUpdateView, self).get_context_data(**kwargs)
        order = Order.objects.get(id=self.kwargs.get('pk'))
        context.update({
            'order': order,
            'table': Table.objects.all().order_by('table_no'),
            'menus': Menu.objects.all().order_by('name')
        })
        return context


class ItemsDetailAPIView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(
            ItemsDetailAPIView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        menus = Menu.objects.all().order_by('name')
        items = []
        for menu in menus:
            item = {
                'id': menu.id,
                'item': menu.name,
                'price': menu.price or 0
            }

            items.append(item)

        return JsonResponse({'items': items})


class GenerateOrderAPIView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(
            GenerateOrderAPIView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        items = json.loads(self.request.POST.get('items'))
        table_no = self.request.POST.get('table_no')
        sub_total = self.request.POST.get('sub_total')
        due_total = self.request.POST.get('grand_total')
        service_charges = self.request.POST.get('service_charges')
        total_qty = self.request.POST.get('totalQty')

        purchased_items_id = []
        with transaction.atomic():
            for item in items:
                menu = Menu.objects.get(name=item.get('item_name'))
                purchased_form_kwargs = {
                    'menu': menu.id,
                    'quantity': item.get('qty'),
                    'price': item.get('price'),
                    'total_price': item.get('total')
                }
                purchased_form = PurchasedMenuItemForm(purchased_form_kwargs)
                if purchased_form.is_valid():
                    purchased_item = purchased_form.save()
                    purchased_items_id.append(purchased_item.id)

            table = Table.objects.get(table_no=table_no)
            order_form_kwargs = {
                'table': table.id,
                'sub_total': sub_total,
                'total_due': due_total,
                'total_qty': total_qty,
                'service_charges': service_charges,
                'items': purchased_items_id,

            }

            order_form = OrderForm(order_form_kwargs)

            if order_form.is_valid():
                order_form.save()

        return JsonResponse({'success': 'Success Message'})


class UpdateOrderAPIView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(
            UpdateOrderAPIView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        items = json.loads(self.request.POST.get('items'))
        table_no = self.request.POST.get('table_no')
        sub_total = self.request.POST.get('sub_total')
        due_total = self.request.POST.get('grand_total')
        service_charges = self.request.POST.get('service_charges')
        total_qty = self.request.POST.get('totalQty')
        purchased_items_id = []

        with transaction.atomic():
            for item in items:
                if item.get('item_id'):
                    purchase_item = (
                        PurchaseMenuItem.objects.get(id=item.get('item_id'))
                    )
                    menu = Menu.objects.get(name=item.get('item_name'))
                    purchase_item.menu = menu
                    purchase_item.quantity = item.get('qty')
                    purchase_item.price = item.get('price')
                    purchase_item.total_price = item.get('total')
                    purchase_item.save()
                    purchased_items_id.append(purchase_item)
                else:
                    menu = Menu.objects.get(name=item.get('item_name'))
                    purchased_form_kwargs = {
                        'menu': menu.id,
                        'quantity': item.get('qty'),
                        'price': item.get('price'),
                        'total_price': item.get('total')
                    }
                    purchased_form = PurchasedMenuItemForm(
                        purchased_form_kwargs)
                    if purchased_form.is_valid():
                        purchased_item = purchased_form.save()
                        purchased_items_id.append(purchased_item)

            table = Table.objects.get(table_no=table_no)
            order_obj = Order.objects.get(id=self.kwargs.get('pk'))
            order_obj.sub_total = sub_total
            order_obj.total_due = due_total
            order_obj.table = table
            order_obj.service_charges = service_charges
            order_obj.total_qty = total_qty
            order_obj.items = purchased_items_id
            order_obj.save()

        return JsonResponse({'success': 'Success Message'})
