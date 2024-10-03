from django import forms
from sales.models import Bill, Order, Customer

from datetime import datetime

class BillForm(forms.ModelForm):
    number_bill = forms.CharField(
        label='Numero de factura', 
        max_length=20, 
        required=True, 
        widget=forms.TextInput()
    )
    customer = forms.CharField(
        label='cliente', 
        max_length=32, 
        required=True,
    )
    sale_date = forms.DateField(
        label='fecha de facturacion', 
        required=True
    )
    
    class Meta:
        model = Bill
        fields = ("number_bill","customer","total_amount","sale_date")
    
    def __init__(self, *args, **kwargs):
        super(BillForm, self).__init__(*args, **kwargs)
        
        self.fields['number_bill'].initial = self.set_number_invoice()
        self.fields['sale_date'].initial = datetime.now()
        self.fields['customer'].initial = self.set_customer()
        # self.fields['customer'].widget.attrs['style'] = 'display:none;'
        
    def set_number_invoice(self):
        last_number_bill = Bill.objects.count()
        new_number_bill = 54000 + last_number_bill + 1
        return f'SF{new_number_bill}'
    
    def set_customer(self):
        return Customer.objects.first().id

class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ("bill","product","quantity","price")
