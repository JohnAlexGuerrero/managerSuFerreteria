from django.db import models
from django.urls import reverse
from main.models import Product, Inventory

# Create your models here.
class Customer(models.Model):
    customer_name = models.CharField(max_length=60, blank=True)
    customer_mobile = models.CharField(max_length=50)
    customer_address = models.TextField()
    email = models.EmailField(max_length=254, blank=True, null=True)
    id_document = models.CharField(max_length=30, unique=True, default='')

    class Meta:
        verbose_name = ("Customer")
        verbose_name_plural = ("Customers")

    def __str__(self):
        return self.customer_name

    def get_absolute_url(self):
        return reverse("Customer_detail", kwargs={"pk": self.pk})


class Bill(models.Model):
    number_bill = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    total_amount = models.FloatField(blank=True, null=True, default=0)
    is_paid = models.BooleanField(default=True)
    
    sale_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = ("Bill")
        verbose_name_plural = ("4. Ventas")
        ordering = ('-number_bill',)

    def __str__(self):
        return self.number_bill

    def get_absolute_url(self):
        return reverse("Bill_detail", kwargs={"pk": self.pk})
    
    def subTotal(self):
        orders = Order.objects.filter(bill__id=self.id)
        subtotal = [x.total_amount for x in orders]
        return round(sum(subtotal) / 1.19)
    
    def getItemsInOrder(self):
        return Order.objects.filter(bill_id=self.id)

class Order(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    price = models.FloatField()
    total_amount = models.FloatField(editable=False, default=0)

    class Meta:
        verbose_name = ("Bill")
        verbose_name_plural = ("5. Pedidos")
    
    def __str__(self) -> str:
        return self.bill.number_bill
    
    def save(self, *args, **kwargs):
        self.total_amount = self.price * self.quantity
        super(Order, self).save(*args, **kwargs)
        
        bill = Bill.objects.get(id=self.bill.id)
        bill.total_amount += self.total_amount
        bill.save()
        
        inventory = Inventory.objects.filter(
            product=self.product
        ).order_by('-id').first()

        totalBal = 0
        if inventory:
            totalBal = inventory.total_balance_quantity - self.quantity
        
        Inventory.objects.create(
            product = self.product,
            sale_quantity = self.quantity,
            purchase_quantity = 0,
            total_balance_quantity = totalBal
        )
