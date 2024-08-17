from django.shortcuts import render
from django.http import JsonResponse

from main.models import Product

# Create your views here.
def list_products(request):
    items = Product.objects.all()
    return JsonResponse({
        "items":[
            {
                "id":item.id,
                "title":item.title,
                "price":item.price
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
                "price":item.price
            }
            for item in items
        ]
    })