from django.urls import path
from sales.views import home, invoice, add_cart, add_order, payment_invoice, list_order, plus_item, minus_item
from sales.views import search_customer, filters_customers, select_customer
from sales.views import BillCreateView

urlpatterns = [
    path('', home, name='home'),
    # path('invoices/new/', create_invoice, name='new_invoice'),
    path('invoices/new/', BillCreateView.as_view(), name='new_invoice'),
    path('invoice/<int:pk>/', invoice, name='invoice'),
    path('invoices/p/<int:pk>/add/', add_cart, name='add_cart'),
    path('invoices/order/add/', add_order, name='add_order'),
    path('invoices/order/<int:pk>/plus/', plus_item, name='plus_item'),
    path('invoices/order/<int:pk>/minus/', minus_item, name='minus_item'),
    path('invoice/<int:pk>/list/order/', list_order, name='list_order'),
    
    path('customers/', search_customer, name='customer_search'),
    path('customers/search', filters_customers, name='customer_filters'),
    path('customers/<int:pk>/select/', select_customer, name='customer_selected'),

    path('invoices/factura/<int:pk>/payment/', payment_invoice, name='invoice_pay'),
]
