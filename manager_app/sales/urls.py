from django.urls import path
from sales.views import create_bill, home

urlpatterns = [
    path('', home, name='home'),
    path('invoices/new/', create_bill, name='invoice_new'),

]
