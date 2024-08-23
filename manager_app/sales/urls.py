from django.urls import path
from sales.views import create_bill, home, list_bills, total_balance, detail_invoice
from main.views import list_products, filter_products

urlpatterns = [
    path('', home, name='home'),
    path('invoices/new/', create_bill, name='invoice_new'),

    # api route
    path('sales/list-invoices/', list_bills, name='list-invoices'),
    path('sales/invoice/<str:number_bill>/', detail_invoice, name='detail-invoice'),
    
    path('sales/list-invoices/balance/', total_balance, name='list-invoices-balance'),
    
    path('inventory/products/',list_products,name='products'),
    path('inventory/products/search',filter_products,name='filter_products'),
]
