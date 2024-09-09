from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Sum

from datetime import datetime

import io
import openpyxl
from openpyxl.writer.excel import save_workbook #.writer.excel import save_virtual_workbook

from sales.models import Bill, Order
from main.models import Purchase
from cash_register.models import Transaction

from sales.forms import BillForm, OrderForm
from django.http import JsonResponse, HttpResponse

# Create your views here.
def list_bills(request):
    bills = Bill.objects.all().order_by('-sale_date')
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

def detail_invoice(request, *args, **kwargs):
    bill = Bill.objects.get(number_bill=kwargs['number_bill'])
    if bill:
        products = Order.objects.filter(bill=bill)
        
    return JsonResponse({
        "number_bill": bill.number_bill,
        "date": bill.sale_date,
        "customer":{
            "num_id": bill.customer.id_document,
            "name":bill.customer.customer_name,
            "address": bill.customer.customer_address,
            "phone": bill.customer.customer_mobile,
            "email": bill.customer.email,
        },
        "products":[
                {
                    "code": item.product.codebar,
                    "description": item.product.title,
                    "qty": item.quantity,
                    "price": item.price,
                    "total": item.total_amount,
                    "tax": 19
                }
                for item in products
            ],
        "subtotal": bill.subTotal(),
        "tax": (bill.total_amount - bill.subTotal()),
        "total": bill.total_amount,
    })

def create_bill(request):
    return render(request, 'invoices/create_bill.html', {
        # 'form': form,
        # 'order_formset': order_formset
    })

def export_csv(request):
    data = {
        'factura':[],
        'cliente':[],
        'total':[],
        'estado':[],
        'fecha':[],
    }
        
    columns = ['factura','cliente','total','estado','fecha']

    for sale in Bill.objects.all():
        data['factura'].append(sale.number_bill),
        data['cliente'].append(sale.customer.customer_name)
        data['total'].append(sale.total_amount)
        if sale.is_paid:
            data['estado'].append('cancelado')
        else:
            data['estado'].append('pendiente')
        data['fecha'].append(sale.sale_date)
    #CSV Data
    import pandas as pd
    df = pd.DataFrame(data=data, columns=columns, index=False)
    file = df.to_csv("ventas.csv")
    return render(request, 'home', file)

#filter data by date
def filter_by_date(request):
    start_date, end_date = request.GET.get('query'), request.GET.get('q')
    bills = Bill.objects.filter(sale_date__range=(start_date, end_date))

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
            for bill in bills
        ]
    })

def export_excel(request):
    template_name = 'invoices/index.html'

    data = {
        'factura':[],
        'cliente':[],
        'total':[],
        'estado':[],
        'fecha':[],
    }
        
    columns = ['factura','cliente','total','estado','fecha']

    for sale in Bill.objects.all():
        data['factura'].append(sale.number_bill),
        data['cliente'].append(sale.customer.customer_name)
        data['total'].append(sale.total_amount)
        if sale.is_paid:
            data['estado'].append('cancelado')
        else:
            data['estado'].append('pendiente')
        data['fecha'].append(sale.sale_date)
    
    #CSV Data
    import pandas as pd
    df = pd.DataFrame(data=data, columns=columns, index=[x for x in range(len(data['factura']))])
    # file = df.to_excel("ventas.xlsx", sheet_name='Ventas', header=True, index=False)
    

    # Usar un buffer en memoria para almacenar el archivo XLSX temporalmente
    buffer = io.BytesIO()
    
    # Escribir el DataFrame en el buffer como un archivo Excel
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Datos')

    # Obtener el contenido del buffer
    buffer.seek(0)
    
    # Crear una respuesta HTTP con el archivo xlsx
    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=my_pandas_data.xlsx'
    
    return response