from django import template

register = template.Library()

@register.filter(name='count_invoices')
def count_invoices(objects):
    return f'There are {len(objects)} invoices'