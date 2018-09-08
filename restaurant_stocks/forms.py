from django import forms

from restaurant_stocks.models import StockIn, StockOut, Stock


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'


class StockInForm(forms.ModelForm):
    class Meta:
        model = StockIn
        fields = '__all__'


class StockOutForm(forms.ModelForm):
    class Meta:
        model = StockOut
        fields = '__all__'
