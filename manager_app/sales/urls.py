from django.urls import path
from sales.views import create_bill, home, invoice, add_cart, add_order

urlpatterns = [
    path('', home, name='home'),
    path('invoices/new/', create_bill, name='invoice_new'),
    path('invoices/<int:pk>/', invoice, name='invoice'),
    path('invoices/p/<int:pk>/add/', add_cart, name='add_cart'),
    path('invoices/order/add/', add_order, name='add_order'),

]
