from django import forms
from restaurant_menu.models import Menu, Category, PurchaseMenuItem


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ('name', 'price',)


class PurchasedMenuItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseMenuItem
        fields = '__all__'
