from django import template
from datetime import datetime

register = template.Library()

@register.filter(name='format_date_hour')
def format_date_hour(value):
    format_date = '%d de %b, %Y | %I : %S %p'
    return datetime.strptime(value, format_date)