from django.urls import path

from cart.views import CartView, add_item_cart, clean_cart

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add/item/plus', add_item_cart, name='add_item_cart'),
    path('clean/', clean_cart, name="clean_cart"),
]
