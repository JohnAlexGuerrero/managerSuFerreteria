from .models import Tax, Inventory
from django import forms

class TaxForm(forms.ModelForm):
    
    class Meta:
        model = Tax
        fields = ("tax_name",)
class InventoryStockForm(forms.ModelForm):
    
    class Meta:
        model = Inventory
        fields = ("product","total_balance_quantity",)

