from django.contrib import admin
from django.shortcuts import redirect

from django.http import HttpRequest

from sales.models import Bill, Customer, Order
from cash_register.models import Transaction

from django.db.models import Sum, Count

import csv

# Register your models here.
admin.site.register(Customer)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['bill','product','quantity','unit','price','total_amount', 'pct_ganancia']
    list_per_page = 10
    list_filter = ['bill__sale_date',]
    search_fields = ['product__title','bill__number_bill']

    def unit(self, obj):
        return obj.product.unit
    
    def pct_ganancia(self, obj):
        return f'{((obj.price - obj.product.price) / obj.price) * 100:,.1f} %'
    # model = Order
    # extra = 1

# @admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['number_bill', 'customer','total_amount', 'sale_date','is_paid','total_sales_amount','balance','is_delivery']
    search_fields = ['number_bill','sale_date']
    list_editable = ['is_paid','is_delivery']
    list_filter = ['sale_date']
    list_per_page = 10
    actions = ['export_sales_csv',]
    total_balance_amount = []

    def total_sales_amount(self, obj):
        # cuenta el total de facturas a tener encuenta
        bill_count = Bill.objects.all().count()
        
        if len(self.total_balance_amount) < bill_count:
            self.total_balance_amount.append(self.balance(obj))
        return sum(self.total_balance_amount)
    
    def balance(self, obj):
        payments = Transaction.objects.filter(bill__number_bill=obj.number_bill).aggregate(Sum('total'))['total__sum']
        if payments:
            return obj.total_amount - payments
        return obj.total_amount
    
    #actions for admin sales
    @admin.action(description='Export to CSV')
    def export_sales_csv(modeladmin, request, queryset):
        data = {
            'factura':[],
            'cliente':[],
            'total':[],
            'estado':[],
            'fecha':[],
        }
        
        columns = ['factura','cliente','total','estado','fecha']

        for sale in queryset:
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
        df.to_csv("ventas.csv")
    
    
admin.site.register(Bill, BillAdmin)