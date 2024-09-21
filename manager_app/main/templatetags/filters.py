from django import template

register = template.Library()

@register.filter(name="calc_price_unit")
def calc_price_unit(value, list_price):
    return round(value / list_price)

@register.filter(name="calculate_total")
def calculate_total(value, qty):
    return round(value * qty)

@register.filter(name='format_price')
def format_price(value):
    return f'$ {value:,.1f}'

@register.filter(name='format_capitalize')
def format_capitalize(description):
    result = ''
    
    for text in [w.capitalize() for w in description.split(' ')]:
        result += f'{text} '
    return result
