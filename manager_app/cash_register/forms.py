from django import forms
from cash_register.models import Transaction

class TransactionForm(forms.ModelForm):
    
    class Meta:
        model = Transaction
        fields = ("transaction_date","bill","total","payment_method")
