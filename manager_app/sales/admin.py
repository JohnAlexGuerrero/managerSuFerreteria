from django.contrib import admin
from django.shortcuts import redirect

from django.http import HttpRequest

from sales.models import Bill, Customer, Order
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
    total_amount = []
    list_display = ['number_bill', 'customer','total_amount', 'sale_date','is_paid','total_sales_amount']
    search_fields = ['number_bill','sale_date']
    # list_editable = ['is_paid']
    list_filter = ['sale_date']
    list_per_page = 10
    actions = ['export_sales_csv',]

    def total_sales_amount(self, obj):
        total_amount_sales = Bill.objects.filter(sale_date=obj.sale_date).aggregate(Sum('total_amount'))['total_amount__sum']
        return total_amount_sales
    
    
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