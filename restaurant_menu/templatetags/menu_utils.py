from django import template

register = template.Library()


@register.simple_tag
def add(a, b):
    return a+b


@register.simple_tag
def subtract(a, b):
    return a-b
