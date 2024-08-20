from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Sum

from sales.models import Bill, Order
from main.models import Purchase
from cash_register.models import Transaction

from sales.forms import BillForm, OrderForm
from django.http import JsonResponse

# Create your views here.


def home(request):
    template_name = 'invoices/index.html'
    return render(request, template_name)

def list_bills(request):
    bills = Bill.objects.all().order_by('-id')
    paginator = Paginator(bills, 8)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return JsonResponse({
        "data": [
            {
                "id": bill.id,
                "number_bill": bill.number_bill,
                "customer": bill.customer.customer_name,
                "value": f'{bill.total_amount:,.0f}',
                "date": bill.sale_date,
                "is_paid": bill.is_paid,
                "method": Transaction.objects.get(bill=bill).payment_method.capitalize()
            }
            for bill in page_obj
        ],
        "pages": page_obj.paginator.num_pages
    })

def total_balance(request):
    total_sales = Transaction.objects.all().aggregate(Sum('total'))['total__sum']
    item_order = Order.objects.filter(bill__is_paid=True)
    total_cost_sales = [(x.quantity * x.product.price) for x in item_order]
    print(total_cost_sales)
    total_balance = total_sales - sum(total_cost_sales)
    return JsonResponse({
        "balance": f'{total_balance:,.0f}',
        "pct_balance": f'{((total_balance / total_sales) * 100):,.1f}',
        "ventas": f'{total_sales:,.0f}',
        "costos": f'{sum(total_cost_sales):,.0f}'
    })

def create_bill(request):
    return render(request, 'invoices/create_bill.html', {
        # 'form': form,
        # 'order_formset': order_formset
    })