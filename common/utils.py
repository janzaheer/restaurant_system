from django.core.cache import cache


def flush():
    # This works as advertised on the memcached cache:
    cache.clear()

