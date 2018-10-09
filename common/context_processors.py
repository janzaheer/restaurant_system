from django.conf import settings


def settings_context(request):
    context = {
        'RESTAURANT_NAME': settings.RESTAURANT_NAME,
        'RESTAURANT_TAG': settings.RESTAURANT_TAG,
        'RESTAURANT_SHORT_NAME': settings.RESTAURANT_SHORT_NAME,
        'RESTAURANT_ADDRESS': settings.RESTAURANT_ADDRESS,
    }
    return context
