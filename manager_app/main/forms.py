from .models import Tax
from django import forms

class TaxForm(forms.ModelForm):
    
    class Meta:
        model = Tax
        fields = ("tax_name",)
