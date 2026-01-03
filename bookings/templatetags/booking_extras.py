from django import template

register = template.Library()

@register.filter(name='currency')
def currency(value, symbol='$'):
    try:
        return f"{symbol}{float(value):.2f}"
    except (ValueError, TypeError):
        return value