from django.contrib import admin
from .models import Product, Unit, Vendor, Purchase,Tax, Inventory, Category, ListPrice
from .forms import TaxForm
from django.db.models import Count, Sum

# Register your models here.
admin.site.register(Unit)
admin.site.register(Vendor)
admin.site.register(ListPrice)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name_category','items','total_amount']
    
    def items(self, obj):
        return obj.count_items()
    
    def total_amount(self, obj):
        total_sum = 0
        items = Product.objects.filter(category__name_category=obj)
        for item in items:
            item_inventory = Inventory.objects.filter(product=item).order_by('-id').first()
            total_sum += (item.price * item_inventory.total_balance_quantity)
        return f'$ {total_sum:,.1f}'    

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    form = TaxForm

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['codebar','title','balance_stock','unit','vlr_unit','list_price']
    search_fields = ['title','category__name_category']
    list_filter = ['category']
    list_per_page = 10

    def vlr_unit(self, obj):
        return f'$ {round(obj.price / obj.list_price.list_price_value):,.0f}'
        
    def balance_stock(self, obj):
        count_quantity = 0
        inventory = Inventory.objects.filter(product=obj.id).order_by('-id')
        for x in inventory:
            return x.total_balance_quantity

#listado de proveedores y compras hechas a cada proveedor
@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['number_purchase','vendor','product','quantity','price','iva','vlr_uni','total_amount','purchase_date']
    search_fields = ['product__title','vendor__name']
    list_filter = ['purchase_date']
    list_per_page = 20

    def iva(self, obj):
        return f'{obj.tax}'
    
    def vlr_uni(self, obj):
        return f'{(obj.price * obj.tax.tax_value):,.0f}'

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    search_fields = ['product__title',]
    list_display = ['product','purchase_quantity','sale_quantity','product_unit','total_balance_quantity','created_at']
    list_filter = ['product__category']

    
