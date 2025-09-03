from django import template

register = template.Library()

@register.filter
def round_number(value):
    try:
        return round(value)
    except:
        return 0
