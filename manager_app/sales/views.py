from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Sum

from sales.models import Bill
from main.models import Purchase

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
                "value": bill.total_amount,
                "date": bill.sale_date,
                "is_paid": bill.is_paid
            }
            for bill in page_obj
        ],
        "pages": page_obj.paginator.num_pages
    })

def total_balance(request):
    total_sales = Bill.objects.all().aggregate(Sum('total_amount'))['total_amount__sum']
    total_purchase = Purchase.objects.all().aggregate(Sum('total_amount'))['total_amount__sum']
    total_balance = total_sales - total_purchase
    return JsonResponse({
        "balance": total_balance,
        "ventas": total_sales,
        "compras": total_purchase
    })

def create_bill(request):
    if request.method == 'POST':
        form = BillForm(request.POST)
        order_formset = OrderForm(request.POST)
    else:
        form = BillForm()
        order_formset = OrderForm()
        
    return render(request, 'invoices/create_bill.html', {
        'form': form,
        'order_formset': order_formset
    })