def last_orders():
    from restaurant_sales.models import Order
    from django.utils import timezone
    from dateutil.relativedelta import relativedelta

    date_time = timezone.now()
    yestarday = date_time

    orders = Order.objects.filter(
        created_at__day=date_time.day,
        created_at__month=date_time.month,
        created_at__year=date_time.year
    )
    print orders