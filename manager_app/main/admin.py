from django.contrib import admin
from .models import Product, Unit, Vendor, Sale, Purchase,Tax, Inventory, Category, ListPrice
from .forms import TaxForm

# Register your models here.
admin.site.register(Unit)
admin.site.register(Vendor)
admin.site.register(ListPrice)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name_category',]
    

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    form = TaxForm

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['codebar','title','balance_stock','unit','vlr_unit','list_price']
    search_fields = ['title','category__name_category']

    def vlr_unit(self, obj):
        return f'$ {round(obj.price / obj.list_price.list_price_value):,.0f}'
        
    def balance_stock(self, obj):
        count_quantity = 0
        inventory = Inventory.objects.filter(product=obj.id).order_by('-id')
        for x in inventory:
            return x.total_balance_quantity

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'product', 'quantity', 'price', 
    'total_amount', 'sale_date']
    search_fields = ['product__title']

#listado de proveedores y compras hechas a cada proveedor
@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['vendor','product','quantity','price','iva','vlr_uni','total_amount','purchase_date']
    search_fields = ['product__title']

    def iva(self, obj):
        return f'{obj.tax}'
    
    def vlr_uni(self, obj):
        return f'{(obj.price * obj.tax.tax_value):,.0f}'

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    search_fields = ['product__title','product__unit__title',]
    list_display = ['product','product_unit','purchase_date','sale_quantity','total_balance_quantity','vendor','customer']

    
