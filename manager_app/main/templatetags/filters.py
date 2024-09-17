from django import template

register = template.Library()

@register.filter(name="calc_price_unit")
def calc_price_unit(value, list_price):
    return round(value / list_price)

@register.filter(name='format_price')
def format_price(value):
    return f'$ {value:,.0f}'