from django.contrib import admin
from sales.models import Bill, Customer, Order

# Register your models here.
admin.site.register(Customer)


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['number_bill', 'customer','total_amount', 'sale_date']
    search_fields = ['product__title']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['bill','product','quantity','unit','total_amount']

    def unit(self, obj):
        return obj.product.unit
