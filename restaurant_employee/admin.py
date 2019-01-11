
from __future__ import unicode_literals
from django.contrib import admin

from restaurant_employee.models import (EmployeeCreditRecord, Employee)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name','cnic', 'mobile_no', 'gender', 'date_of_joining', 'date_of_leaving',)


class EmployeeCreditRecordAdmin (admin.ModelAdmin):
    list_display = ('employee', 'credit_amount',)


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeCreditRecord,EmployeeCreditRecordAdmin)
