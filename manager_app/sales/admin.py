from django.contrib import admin
from sales.models import Bill, Customer, Order
from django.db.models import Sum, Count

# Register your models here.
admin.site.register(Customer)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['bill','product','quantity','unit','total_amount']
    list_per_page = 10
    list_filter = ['bill__sale_date']

    def unit(self, obj):
        return obj.product.unit
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

    def total_sales_amount(self, obj):
        total_amount_sales = Bill.objects.filter(sale_date=obj.sale_date).aggregate(Sum('total_amount'))['total_amount__sum']
        return total_amount_sales
    
    
admin.site.register(Bill, BillAdmin)