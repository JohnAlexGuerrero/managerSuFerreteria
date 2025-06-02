from django.views.generic import TemplateView

from django.shortcuts import render, redirect
from main.models import Product

items_in_order = []

class CartView(TemplateView):
    template_name = "cart/index.html"
    
    def get_context_data(self, **kwargs) -> dict[str, object]:
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all() 
        return context
    
    
def add_order_product(request, pk):
    name_template = "includes/cart.html"
    product = Product.objects.get(pk=pk)
    
    items_in_order.append({
        "id": product.id,
        "title": product.title,
        "qty": 1,
        "price": product.price,
        "total": (product.price * 1) 
    })

    context = {
        "message":"producto agregado a carrito de compras.",
        "items": items_in_order,
        "total": sum([x['total'] for x in items_in_order])
    }
    
    return render(request, name_template, context)
    
    
def add_item_cart(request):
    name_template = 'cart/partials/list.html'
 
    for item in items_in_order:
        if item['id'] == int(request.POST.get('pk')):
            item['qty'] = item['qty'] + 1
            item['total'] = item['qty'] * item['price']
        else:
            continue
    
    context = {
        "items": items_in_order,
        "total": sum([x['total'] for x in items_in_order])
    }
    
    return render(request, name_template, context)