from django.shortcuts import render
from sales.models import Bill
from sales.forms import BillForm, OrderForm
from django.http import JsonResponse

# Create your views here.


def home(request):
    template_name = 'invoices/index.html'
    return render(request, template_name)

def list_bills(request):
    bills = Bill.objects.all().order_by('-id')
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
            for bill in bills
        ]  
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