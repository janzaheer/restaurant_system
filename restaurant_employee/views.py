# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Employee
from django.views.generic import FormView,UpdateView
from restaurant_employee.forms import Employee_form
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.views.generic import TemplateView


class EmployeeRecordView(TemplateView):
    template_name = 'employee/employee_record.html'

    def get_context_data(self, **kwargs):
        context = super(EmployeeRecordView, self).get_context_data(**kwargs)
        employee = Employee.objects.all()
        context.update({
            'employees': employee
        })
        return context


class AddEmployeeView(FormView):
    form_class = Employee_form
    template_name = 'employee/add_employee.html'

    def form_valid(self, form):
        print "-----------comiong here bro------------"
        form.save()
        return HttpResponseRedirect(reverse('employee_record'))
    
    def form_invalid(self, form):
        print "---------------- error--------------"
        print "---------------- error--------------"
        print "---------------- error--------------"
        print form.errors
        return super(AddEmployeeView, self).form_invalid(form)
