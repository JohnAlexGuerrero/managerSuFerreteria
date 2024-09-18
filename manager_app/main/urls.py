from django.urls import path
from main.views import list_products, filter_products
from main.views import inventory, product_detail, inventory_create, selected_product, export_data_inventory

urlpatterns = [
    path('products/', inventory, name='inventory'),
    path('products/<int:pk>/detail/', product_detail, name='product_detail'),
    path('products/<int:pk>/edit/', inventory_create, name='product_edit'),
    path('products/<int:pk>/select/', selected_product, name='selected_product'),
    path('products/selected/', export_data_inventory, name='get_product_selected'),
]

