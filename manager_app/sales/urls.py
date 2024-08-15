from django.urls import path
from sales.views import create_bill, home, list_bills

urlpatterns = [
    path('', home, name='home'),
    path('invoices/new/', create_bill, name='invoice_new'),
    path('list-invoices/', list_bills, name='list-invoices'),
]
