from django import forms
from sales.models import Bill, Order


class BillForm(forms.ModelForm):
    
    class Meta:
        model = Bill
        fields = ("number_bill","customer","total_amount")

class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ("bill","product","quantity","price")
