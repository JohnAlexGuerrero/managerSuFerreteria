from django.urls import path
from api.views import list_bills, total_balance, detail_invoice, export_excel, filter_by_date
from main.views import list_products, filter_products

urlpatterns = [

    # api route
    path('sales/list-invoices/', list_bills, name='list-invoices'),
    path('sales/invoice/<str:number_bill>/', detail_invoice, name='detail-invoice'),
    path('sales/list-invoices/filter/date', filter_by_date, name='filter_date'),
    path('sales/list-invoices/balance', total_balance, name='list-invoices-balance'),
    
    path('inventory/products/',list_products,name='products'),
    path('inventory/products/search',filter_products,name='filter_products'),
        
    path('export_csv/', export_excel, name='export_csv'),
    
]