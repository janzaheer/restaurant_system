"""resturant_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from common.views import DashboardView, ReportsView
from restaurant_menu.views import (
    CategoryList, CategoryFormView, CategoryUpdateView, CategoryDeleteView,
    MenuListView, MenuFormView, MenuUpdateView, MenuDeleteView,
    MenuItemPurchasedLogsView, PurchasedDetailedLogsView
)
from restaurant_sales.views import (
    TableListView, TableFormView, TableUpdateView, TableDeleteView,
    OrderListView, OrderCreateView, OrderUpdateView, OrderView,
    ItemsDetailAPIView, GenerateOrderAPIView, UpdateOrderAPIView
)
from restaurant_stocks.views import (
    StockListView, StockFormView, StockInFormView, StockOutFormView,
    StockDetailView, CloseStockView, StockClosedItemLogsView
)

from common.reports_api import (
    DailyOrdersAPIView, MonthlyOrderAPIView,
    DailyStocksAPIView, MonthlyStocksAPIView,
    StockCLosedAPIView,
)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', DashboardView.as_view(), name='dashboard'),

    # Category URLS
    url(
        r'^category/add/$',
        CategoryFormView.as_view(), name='category_add'
    ),
    url(
        r'^category/(?P<pk>\d+)/update/$',
        CategoryUpdateView.as_view(),
        name='category_update'
    ),
    url(
        r'^category/(?P<pk>\d+)/delete/$',
        CategoryDeleteView.as_view(),
        name='category_delete'
    ),
    url(
        r'^category/list/$', CategoryList.as_view(),
        name='category_list'
    ),

    # Menu Urls
    url(
        r'^menu/list/$', MenuListView.as_view(),
        name='menu_list'
    ),
    url(
        r'^menu/add/$', MenuFormView.as_view(),
        name='menu_add'
    ),
    url(
        r'^menu/(?P<pk>\d+)/update/$',
        MenuUpdateView.as_view(),
        name='menu_update'
    ),
    url(
        r'^menu/(?P<pk>\d+)/delete/$',
        MenuDeleteView.as_view(),
        name='menu_delete'
    ),

    # Table Urls
    url(
        r'^table/list/$', TableListView.as_view(),
        name='table_list'
    ),
    url(
        r'^table/add/$', TableFormView.as_view(),
        name='table_add'
    ),
    url(
        r'^table/(?P<pk>\d+)/update/$',
        TableUpdateView.as_view(),
        name='table_update'
    ),
    url(
        r'^table/(?P<pk>\d+)/delete/$',
        TableDeleteView.as_view(),
        name='table_delete'
    ),

    # Order Urls
    url(
        r'^order/list/$', OrderListView.as_view(),
        name='order_list'
    ),
    url(
        r'^order/create/$', OrderCreateView.as_view(),
        name='order_create'
    ),
    url(
        r'^order/(?P<pk>\d+)/update/$',
        OrderUpdateView.as_view(),
        name='order_update'
    ),
    url(
        r'^order/(?P<pk>\d+)/view/$',
        OrderView.as_view(),
        name='order_view'
    ),

    # API Urls
    url(
        r'^item/details/api/$', ItemsDetailAPIView.as_view(),
        name='item_details_api'
    ),
    url(
        r'^order/generate/api/$', GenerateOrderAPIView.as_view(),
        name='order_generate_api'
    ),
    url(
        r'^order/(?P<pk>\d+)/update/api/$',
        UpdateOrderAPIView.as_view(),
        name='order_update_api'
    ),
    url(
        r'^closed/stock/api/$', StockCLosedAPIView.as_view(),
        name='closed_stock_api'
    ),

    # Reports Url
    url(
        r'^reports/$', ReportsView.as_view(),
        name='reports'
    ),

    # Reports API Endpoints
    url(
        r'^orders/daily/api/$', DailyOrdersAPIView.as_view(),
        name='daily_orders'
    ),
    url(
        r'^orders/monthly/api/$', MonthlyOrderAPIView.as_view(),
        name='monthly_orders'
    ),
    url(
        r'^stocks/daily/api/$', DailyStocksAPIView.as_view(),
        name='daily_stocks'
    ),
    url(
        r'^stocks/monthly/api/$', MonthlyStocksAPIView.as_view(),
        name='monthly_stocks'
    ),

    # Logs Url
    url(
        r'^logs/$', MenuItemPurchasedLogsView.as_view(),
        name='logs'
    ),
    url(
        r'^logs/(?P<date>[a-zA-Z0-9_-]+)/$',
        MenuItemPurchasedLogsView.as_view(),
        name='logs_date'
    ),
    url(
        r'^detailed/logs/$', PurchasedDetailedLogsView.as_view(),
        name='detailed_logs'
    ),
    url(
        r'^detailed/logs/(?P<date>[a-zA-Z0-9_-]+)/$',
        PurchasedDetailedLogsView.as_view(),
        name='detailed_logs_date'
    ),

    # Stocks Url
    url(
        r'^stock/list/$', StockListView.as_view(),
        name='stock_list'
    ),
    url(
        r'^stock/new/$', StockFormView.as_view(),
        name='stock_new'
    ),
    url(
        r'^stock/(?P<pk>\d+)/in/$',
        StockInFormView.as_view(),
        name='stock_in'
    ),
    url(
        r'^stock/(?P<pk>\d+)/out/$',
        StockOutFormView.as_view(),
        name='stock_out'
    ),
    url(
        r'^stock/(?P<pk>\d+)/details/$',
        StockDetailView.as_view(),
        name='stock_details'
    ),
    url(
        r'^stock/closed/$', CloseStockView.as_view(),
        name='close_stock'
    ),
    url(
        r'^stock/(?P<pk>\d+)/closed/logs/$',
        StockClosedItemLogsView.as_view(),
        name='closed_item_logs'
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
