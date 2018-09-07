# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import (
    FormView, TemplateView, RedirectView, UpdateView, DeleteView
)
from django.http import HttpResponseRedirect

from restaurant_menu.models import Menu, Category
from restaurant_menu.forms import CategoryForm, MenuForm

from django.core.urlresolvers import reverse, reverse_lazy


class MenuFormView(FormView):
    template_name = 'menu/add.html'
    form_class = MenuForm

    def __init__(self, *args, **kwargs):
        super(MenuFormView, self).__init__(*args, **kwargs)
        self.error_message = ''

    def get_context_data(self, **kwargs):
        context = super(MenuFormView, self).get_context_data(**kwargs)
        context.update({
            'categories': Category.objects.all().order_by('name'),
        })
        return context

    def form_valid(self, form):
        menu = form.save(commit=False)
        try:
            category = Category.objects.get(
                name=self.request.POST.get('category'))
        except Category.DoesNotExist:
            return self.form_invalid(form)
        menu.category = category
        menu.save()

        return HttpResponseRedirect(reverse('menu_list'))

    def form_invalid(self, form):
        return super(MenuFormView, self).form_invalid(form)
    

class MenuUpdateView(UpdateView):
    template_name = 'menu/update.html'
    form_class = MenuForm
    success_url = reverse_lazy('menu_list')
    model = Menu

    def form_valid(self, form):
        menu = form.save(commit=False)
        try:
            category = Category.objects.get(
                name=self.request.POST.get('category'))
        except Category.DoesNotExist:
            return self.form_invalid(form)
        menu.category = category
        menu.save()
        return super(MenuUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(MenuUpdateView, self).get_context_data(**kwargs)
        context.update({
            'categories': Category.objects.all().order_by('name'),
        })
        return context


class MenuDeleteView(DeleteView):
    model = Menu
    success_url = reverse_lazy('menu_list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class MenuListView(TemplateView):
    template_name = 'menu/list.html'

    def get_context_data(self, **kwargs):
        context = super(MenuListView, self).get_context_data(**kwargs)

        context.update({
            'menus': Menu.objects.all().order_by('name')
        })
        return context


class CategoryFormView(FormView):
    template_name = 'category/add.html'
    form_class = CategoryForm

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('category_list'))


class CategoryList(TemplateView):
    template_name = 'category/list.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        context.update({
            'categories': Category.objects.all().order_by('name')
        })
        return context


class CategoryUpdateView(UpdateView):
    template_name = 'category/update.html'
    form_class = CategoryForm
    model = Category
    success_url = reverse_lazy('category_list')


class CategoryDeleteView(DeleteView):
    # template_name = 'category/list.html'
    model = Category
    success_url = reverse_lazy('category_list')

    def get_queryset(self):
        return self.model.objects.filter(id=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
