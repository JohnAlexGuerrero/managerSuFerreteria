from django.db import models
from django.db.models import Sum

from django.urls import reverse
from sales.models import Bill

# Create your models here.
    
    
class Transaction(models.Model):
    class PaymentMethod(models.TextChoices):
        EFECTIVO = "EFECTIVO"
        TRANSFERENCIA_BANCARIA = "TRANSFERECIA BANCARIA"
        TARJETA_CREDITO = "TARJETA CREDITO"
        NEQUI = "NEQUI"
        OTROS = "OTROS"
        
    transaction_date = models.DateTimeField(auto_now_add=False)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, null=True, blank=True, related_name='pays')    
    total = models.FloatField(default=0)
    payment_method = models.CharField(max_length=50, choices=PaymentMethod, default=PaymentMethod.EFECTIVO)
    
    class Meta:
        verbose_name = ("Transaction")
        verbose_name_plural = ("Transactions")

    def __str__(self):
        return self.bill.number_bill

    def get_absolute_url(self):
        return reverse("Transaction_detail", kwargs={"pk": self.pk})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.bill.is_paid != True:
            total_pay = self.bill.pays.all().aggregate(Sum('total'))['total__sum']
            balance_res = total_pay - self.total
            if balance_res == 0:
                self.bill.is_paid = True
                self.bill.save()
            return ''
                

