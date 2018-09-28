from django import forms

from restaurant_stocks.models import (
    StockIn, StockOut, Stock,
    StockClosed, StockItemClosed
)


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


class ClosedStockForm(forms.ModelForm):
    class Meta:
        model = StockClosed
        fields = '__all__'


class ClosedStockItemForm(forms.ModelForm):
    class Meta:
        model = StockItemClosed
        fields = '__all__'
