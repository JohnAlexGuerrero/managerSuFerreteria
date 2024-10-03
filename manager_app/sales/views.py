from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Sum
from django.db.models import Q

from datetime import datetime

from django.views.generic import CreateView

from sales.models import Bill, Order, Customer
from main.models import Purchase, Product
from main.views import paginator_products
from cash_register.models import Transaction

from sales.forms import BillForm, OrderForm
from cash_register.forms import TransactionForm

from django.http import JsonResponse

#variables locales
items_in_order = []

# Create your views here.
def home(request):
    template_name = 'invoices/index.html'
    
    context = {
        "today": datetime.now().strftime('%d-%B-%Y')
    }
    print(context)
    
    return render(request, template_name, context)


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

#view CBVs crea una instancia de la factura nueva
class BillCreateView(CreateView):
    model = Bill
    form_class = BillForm
    template_name = "invoices/invoice.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["customer"] = Customer.objects.first()
        context['items'] = Product.objects.all()
        context['orders'] = items_in_order
        return context
    


def create_invoice(request):
    number_bill = f'SF{54000 + Bill.objects.count()}'
    customer = Customer.objects.first()
    new_bill = Bill.objects.create(number_bill=number_bill, customer=customer, sale_date=datetime.now())
    
    return redirect('invoice', kwargs={'pk': new_bill.id})
    
def invoice(request, *args, **kwargs):
    name_template = 'invoices/create_bill.html'
    invoice = get_object_or_404(Bill, pk=kwargs['pk'])
    page_number = request.GET.get("page")
    
    items = paginator_products(page_number)
    
    if invoice:
        orders = Order.objects.filter(bill=invoice)
        context = {
            "invoice":invoice,
            "items": items,
            "orders": orders,
            "customer": invoice.customer
        }
        
        return render(request, name_template, context)
    else:
        redirect('home')
    
#view donde se guarda la informacion de los productos seleccionados
def add_cart(request, *args, **kwargs):
    name_template = 'invoices/cart/list.html'
    item = get_object_or_404(Product, pk=kwargs['pk'])
    
    #funcion que guarda el pedido en memoria cache
    def add_order_in_cart(item):
        order = {
            "id": item.id,
            "product": item.title,
            "codebar": item.codebar,
            "qty": 1,
            "price": item.price,
            "total": 0,
            "list_price": item.list_price.list_price_value
        }
        
        items_in_order.append(order)
        return items_in_order

    context = {
        "item": item,
        "orders": add_order_in_cart(item)
    }

    return render(request, name_template, context)

#view add one item a product in order
def plus_item(request, *args, **kwargs):
    template_name = 'invoices/cart/list.html'
    
    for product in items_in_order:
        if product['id'] == kwargs['pk']:
            product['qty'] += 1
            break

    context = {"orders": items_in_order}
    return render(request, template_name, context)

#view minus one item a product in order
def minus_item(request, *args, **kwargs):
    template_name = 'invoices/cart/list.html'
    
    for product in items_in_order:
        if product['id'] == kwargs['pk']:
            product['qty'] -= 1
            if product['qty'] == 0:
                items_in_order.remove(product)
            break
        
    context = {"orders": items_in_order}
    return render(request, template_name, context)

#view para guardar pedido
def add_order(request):
    template_name = 'invoices/cart/list.html'
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        pk = request.POST.get('bill')
        
        if form.is_valid():
            orders = Order.objects.filter(bill__id=pk)
            form.save()
            context = {
                "orders": orders
            }
            return render(request, template_name, context)
    
#view para listar los productos contenidos en el pedido
def list_order(request, *args, **kwargs):
    template_name = 'invoices/cart/list.html'
    pk = kwargs['pk']
    orders = Order.objects.filter(bill__id=pk)
    
    context = {
        "orders": orders,
    }
    
    return render(request, template_name, context)
                
#view customer search
def search_customer(request):
    template_name = 'customer/partials/search.html'
    return render(request, template_name)

#view filter customers
def filters_customers(request):
    template_name = 'customer/partials/list.html'
    
    customers = Customer.objects.filter(
        Q(customer_name__icontains=request.GET.get('query'))
    )
    
    context = {
        "customers": customers.order_by('customer_name')
    }
    
    return render(request, template_name, context)

#view select customer
def select_customer(request, *args, **kwargs):
    template_name = 'customer/detail.html'
    customer = get_object_or_404(Customer, pk=kwargs['pk'])

    context = {
        # "customer": update_customer_in_invoice(customer)
        "customer": customer
    }
    
    return render(request, template_name, context)

#function update customer in invoice
def update_customer_in_invoice(customer):
    bill = Bill.objects.all().order_by('-id').first()
    bill.customer = customer
    bill.save()
    return bill.customer

#view payment invoice
def payment_invoice(request, *args, **kwargs):
    template_name = 'invoices/payment/pay.html'
    bill = Bill.objects.get(id=kwargs['pk'])
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
          form.save()
          return redirect('home')
    else:
        data = {
            "transaction_date": datetime.now(),
            "bill": bill,
            "total": bill.total_amount,
            "payment_method": ''
        }
        
        form = TransactionForm(initial=data)
        
    context = { "form": form, "bill": bill }
    
    return render(request, template_name, context)