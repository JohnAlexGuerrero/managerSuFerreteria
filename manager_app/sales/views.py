from django.shortcuts import render
from sales.models import Bill
from sales.forms import BillForm, OrderForm

# Create your views here.


def home(request):
    return render(request, 'invoices/index.html')

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