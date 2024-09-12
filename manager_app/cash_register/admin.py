from django.contrib import admin
from cash_register.models import Transaction

# Register your models here.
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_date','bill','total']
