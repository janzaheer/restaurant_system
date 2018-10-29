# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.core.urlresolvers import reverse, reverse_lazy

from django.contrib.auth import forms as auth_forms
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate

from django.views.generic import FormView, TemplateView, RedirectView
from django.http import HttpResponseRedirect
from django.db.models import Sum

from django.utils import timezone

from restaurant_sales.models import Order


class LoginView(FormView):
    template_name = 'login.html'
    form_class = auth_forms.AuthenticationForm
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):

        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('dashboard'))

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user)
        return HttpResponseRedirect(reverse('dashboard'))

    def form_invalid(self, form):
        return super(LoginView, self).form_invalid(form)


class LogoutView(RedirectView):
    def dispatch(self, request, *args, **kwargs):
        auth_logout(self.request)
        return super(LogoutView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('login'))


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            return super(
                DashboardView, self).dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('login'))


class ReportsView(TemplateView):
    template_name = 'reports.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            if (
                self.request.user.user_profile.user_type ==
                self.request.user.user_profile.USER_TYPE_OWNER
            ):
                return super(
                    ReportsView, self).dispatch(request, *args, **kwargs)

        return HttpResponseRedirect(reverse('login'))

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