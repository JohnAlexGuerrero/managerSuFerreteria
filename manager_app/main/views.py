from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator

from main.models import Product, Category, Inventory

from main.forms import InventoryStockForm

#array local
products_selected = []

# Create your views here.
def inventory(request):
    name_template = 'inventory/list_products.html'
    filter_option = request.GET.get('filter','all')
    
    if filter_option == 'all':
        products = Product.objects.all().order_by('-updated_at')
    else:
        products = Product.objects.filter(category__name_category=filter_option).order_by('-updated_at')
        
    context = {
        "inventory": products,
        "categories": [item.name_category for item in Category.objects.all()],
        "filter_option": filter_option,
    }
    
    return render(request, name_template, context)

#view selected product
def selected_product(request, *args, **kwargs):
    name_template = 'inventory/list_products.html'
    product = get_object_or_404(Product, pk=kwargs['pk'])
    add_product_select(product)
    
    context = {
        "count": len(products_selected)
    }
    return render(request, name_template, context)

#view detail product
def product_detail(request, *args, **kwargs):
    name_template = 'product/detail.html'
    product = get_object_or_404(Product, pk=kwargs['pk'])
    context = {
        "product": product
    }
    
    return render(request, name_template, context)

#view edit product
def inventory_create(request, *args, **kwargs):
    name_template = 'inventory/new.html'
    product = get_object_or_404(Product, pk=kwargs['pk'])
    
    if request.method == 'POST':
        form = InventoryStockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("inventory")
    else:
        form = InventoryStockForm()
        
    context = {
        "product": product,
        "form": form
    }
    
    return render(request, name_template, context)

def list_products(request):
    items = Product.objects.all()#.order_by('category')
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

#view para export data
def export_data_inventory(request):
    name_template = 'inventory/list_products.html'
    context = {}
    print(get_product_select())
    return render(request, name_template, context)
    
#function que guarda un producto seleccionado en un array
def add_product_select(product):
    products_selected.append(product)
    
#function que obtiene la informacion del array local que guarda los productos seleccionados
def get_product_select():
    data = [
        {
            "id": item.id,
            "description": item.title,
            "codebar": item.codebar
        }
        for item in products_selected
    ]
    
    return data