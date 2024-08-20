from django.shortcuts import render
from django.http import JsonResponse

from main.models import Product, Category

# Create your views here.
def list_products(request):
    items = Product.objects.all().order_by('category')
    return JsonResponse({
        "items":[
            {
                "id":item.id,
                "title":item.title,
                "price": f'{round((item.price / item.list_price.list_price_value),0):,.0f}',
                "category": str(item.category)
            }
            for item in items
        ]
    })
    
def filter_products(request):
    items = Product.objects.filter(title__contains=request.GET.get('query'))
    return JsonResponse({
        "items":[
            {
                "id":item.id,
                "title":item.title,
                "price": f'{round((item.price / item.list_price.list_price_value),0):,.0f}',
                "category": str(item.category)
            }
            for item in items
        ]
    })