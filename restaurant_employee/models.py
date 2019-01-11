# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class Employee(models.Model):
    name = models.CharField(max_length=200,)
    mobile_no = models.CharField(max_length=200, null=True, blank=True,)
    cnic = models.CharField(max_length=200, null=True, blank=True,)
    gender = models.CharField(max_length=100, null=True, blank=True,)
    date_of_joining = models.DateField(null=True, blank=True,)
    date_of_leaving = models.DateField(null=True, blank=True,)


class EmployeeCreditRecord(models.Model):
    employee = models.CharField(max_length=200,)
    credit_amount = models.DecimalField(
        max_digits=20, decimal_places=2, default=0, blank=True, null=True
    )
    details = models.TextField(max_length=500, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now, null=True, blank=True,)
