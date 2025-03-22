from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views.generic import CreateView

from cash_register.models import Transaction
from cash_register.forms import TransactionForm

# Create your views here.
class TransactionCreateView(CreateView):
    model = Transaction
    template_name = "invoices/payment/pay.html"
    form_class = TransactionForm
    
    def get_success_url(self):
        return reverse_lazy("invoice", kwargs={'pk': self.object.bill_id})
