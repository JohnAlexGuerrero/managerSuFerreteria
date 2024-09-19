from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Sum

from datetime import datetime

from sales.models import Bill, Order, Customer
from main.models import Purchase, Product
from cash_register.models import Transaction

from sales.forms import BillForm, OrderForm
from django.http import JsonResponse

#variables locales
items_in_order = []

# Create your views here.


def home(request):
    template_name = 'invoices/index.html'
    return render(request, template_name)

# def total_balance(request):
#     total_sales = Transaction.objects.all().aggregate(Sum('total'))['total__sum']
#     item_order = Order.objects.filter(bill__is_paid=True)
#     total_cost_sales = [(x.quantity * x.product.price) for x in item_order]
#     print(total_cost_sales)
#     total_balance = total_sales - sum(total_cost_sales)
#     return JsonResponse({
#         "balance": f'{total_balance:,.0f}',
#         "pct_balance": f'{((total_balance / total_sales) * 100):,.1f}',
#         "ventas": f'{total_sales:,.0f}',
#         "costos": f'{sum(total_cost_sales):,.0f}'
#     })

# def detail_invoice(request, *args, **kwargs):
#     print()
#     bill = Bill.objects.get(number_bill=kwargs['number_bill'])
#     if bill:
#         products = Order.objects.filter(bill=bill)
        
#     return JsonResponse({
#         "number_bill": bill.number_bill,
#         "date": bill.sale_date,
#         "customer":{
#             "num_id": bill.customer.id_document,
#             "name":bill.customer.customer_name,
#             "address": bill.customer.customer_address,
#             "phone": bill.customer.customer_mobile,
#             "email": bill.customer.email,
#         },
#         "products":[
#                 {
#                     "code": item.product.codebar,
#                     "description": item.product.title,
#                     "qty": item.quantity,
#                     "price": item.price,
#                     "total": item.total_amount,
#                     "tax": 19
#                 }
#                 for item in products
#             ],
#         "subtotal": bill.subTotal(),
#         "tax": (bill.total_amount - bill.subTotal()),
#         "total": bill.total_amount,
#     })

def create_bill(request):
    number_bill = f'SF{54000 + Bill.objects.count()}'
    customer = Customer.objects.first()
    
    new_bill = Bill.objects.create(number_bill=number_bill, customer=customer, sale_date=datetime(2024,7,1))
    
    if new_bill:
      return redirect('invoice', kwargs={'pk': new_bill.id})
    return redirect('home')
    
    
def invoice(request, *args, **kwargs):
    name_template = 'invoices/create_bill.html'
    
    invoice = get_object_or_404(Bill, pk=kwargs['pk'])
    orders = Order.objects.filter(bill=invoice)

    
    if invoice:
        context = {
            "invoice":invoice,
            "items": Product.objects.all().order_by('title'),
            "orders": orders,

        }
        
        return render(request, name_template, context)
    else:
        redirect('home')
    
#view donde se guarda la informacion de los productos seleccionados
def add_cart(request, *args, **kwargs):
    name_template = 'invoices/cart/form.html'
    item = get_object_or_404(Product, pk=kwargs['pk'])
    bill = Bill.objects.all().order_by('sale_date').first()
    
    if item:
        form = OrderForm()
        
    context = {
        "form": form,
        "item": item,
        "bill":bill
    }
    # return render(request, name_template)
    return render(request, name_template, context)

#view para guardar pedido
def add_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            redirect('invoice', kwargs={'pk': request.POST.get('bill')})