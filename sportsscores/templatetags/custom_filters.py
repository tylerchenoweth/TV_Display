# custom_filters.py
from django import template

register = template.Library()

@register.filter
def group_in_threes(value):
    return [value[i:i+3] for i in range(0, len(value), 3)]
