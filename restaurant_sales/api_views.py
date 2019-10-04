from restaurant_menu.models import Menu
from restaurant_sales.models import Table

from django.views import View
from django.http import JsonResponse


class MenuItemListAPIView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(
            MenuItemListAPIView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        menus = Menu.objects.all().order_by('name')
        items = []
        for menu in menus:
            item = {
                'id': menu.id,
                'item': menu.name,
                'category': menu.category.name,
                'category_id': menu.category.id,
                'price': menu.price or 0
            }
            items.append(item)

        return JsonResponse({'items': items})


class TableListAPIView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(
            TableListAPIView, self
        ).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        tables_obj = Table.objects.all().order_by('table_no')
        tables = []
        for table in tables_obj:
            table = {
                'table_name': table.table_name,
                'table_no': table.table_no,
                'table_type': table.table_type,
                'table_id': table.id,
            }
            tables.append(table)
        return JsonResponse({'tables': tables})
