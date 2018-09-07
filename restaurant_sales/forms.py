from django import forms

from restaurant_sales.models import Table, Order


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = '__all__'


class OrderForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = Order
