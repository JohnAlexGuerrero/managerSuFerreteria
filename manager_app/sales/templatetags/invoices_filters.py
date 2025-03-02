from django import template

register = template.Library()

@register.filter(name='count_invoices')
def count_invoices(objects):
    return f'There are {len(objects)} invoices'

@register.filter(name='status_invoice')
def status_invoice(value):
    return "Cancelado" if value else "Pendiente"

@register.filter(name='delivery_invoice')
def delivery_invoice(value):
    return "Entregado" if value else "Pendiente"

@register.filter(name='get_balance_invoice')
def get_balance_invoice(value_1, value_2):
    return - value_1 + value_2

@register.filter(name='get_total_sum')
def get_total_sum(objects):
    total_sum = [x.total for x in objects]
    return sum(total_sum)