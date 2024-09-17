from django.urls import path
from main.views import list_products, filter_products
from main.views import inventory, product_detail, inventory_create

urlpatterns = [
    path('products/', inventory, name='inventory'),
    path('products/<int:pk>/detail/', product_detail, name='product_detail'),
    path('products/<int:pk>/edit/', inventory_create, name='product_edit'),
]

