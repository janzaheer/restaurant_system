from restaurant_menu.models import Menu

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

