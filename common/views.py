# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render

from django.views.generic import FormView, TemplateView, RedirectView
from django.http import HttpResponseRedirect


class DashboardView(TemplateView):
    template_name = 'dashboard.html'
