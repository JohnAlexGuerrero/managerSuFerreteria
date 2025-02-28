from django import template

register = template.Library()

@register.filter(name='count_invoices')
def count_invoices(objects):
    return f'There are {len(objects)} invoices'

@register.filter(name='status_invoice')
def status_invoice(value):
    return "Cancelado" if value else "Pendiente"