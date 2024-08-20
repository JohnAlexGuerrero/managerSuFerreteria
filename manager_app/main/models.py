from django.db import models
from django.urls import reverse
from django.db.models import Count, Sum
#from sales.models import Bill

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField()
    mobile = models.CharField(max_length=15)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = ("Vendor")
        verbose_name_plural = ("3. Proveedores")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Vendor_detail", kwargs={"pk": self.pk})

class Tax(models.Model):
    tax_name = models.IntegerField()
    tax_value = models.FloatField()

    class Meta:
        verbose_name = ("Tax")
        verbose_name_plural = ("Taxes")
    
    def __str__(self):
        return f'{self.tax_name}%'

    def save(self, *args, **kwargs):
        self.tax_value = 1 +  (self.tax_name / 100)
        return super(Tax, self).save(*args, **kwargs)
    
class Unit(models.Model):
    title = models.CharField(max_length=50, unique=True)
    short_name = models.CharField(max_length=10)

    class Meta:
        verbose_name = ("Unit")
        verbose_name_plural = ("Units")

    def __str__(self):
        return self.short_name

    def get_absolute_url(self):
        return reverse("Unit_detail", kwargs={"pk": self.pk})

class ListPrice(models.Model):
    list_price_name = models.CharField(max_length=50, unique=True)
    list_price_value = models.FloatField()
    
    class Meta:
        verbose_name = ("ListProduct")
        verbose_name_plural = ("ListProducts")
    
    def __str__(self):
        return self.list_price_name

    def save(self, *args, **kwargs):
        self.list_price_value = (100 - self.list_price_value) / 100
        return super(ListPrice, self).save(*args, **kwargs)

class Category(models.Model):
    name_category = models.CharField(max_length=50)

    class Meta:
        verbose_name = ("Category")
        verbose_name_plural = ("Categories")

    def __str__(self):
        return self.name_category

    def count_items(self):
        return Category.objects.filter(name_category=self).aggregate(Count('product'))['product__count']
    
    
class Product(models.Model):
    title = models.CharField(max_length=70, unique=True)
    codebar = models.CharField(max_length=15, unique=True)
    photo = models.ImageField(upload_to="product/", null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True,blank=True)
    price = models.FloatField(null=True,blank=True, default=0)
    list_price = models.ForeignKey(ListPrice, on_delete=models.CASCADE, default=1)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = ("Product")
        verbose_name_plural = ("1. Products")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Product_detail", kwargs={"pk": self.pk})


class Purchase(models.Model):
    number_purchase = models.CharField(max_length=50, unique=False)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    quantity = models.FloatField()
    price = models.FloatField()
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE, null=True)
    total_amount = models.FloatField(editable=False, default=0)
    # status = models.BooleanField(default=False)
    purchase_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = ("Purchase")
        verbose_name_plural = ("3. compras")
    
    def __str__(self):
        return self.number_purchase

    def save(self, *args, **kwargs):
        self.total_amount = self.quantity * self.price
        super(Purchase, self).save(*args, **kwargs)
        
        product = Product.objects.get(id=self.product.id)
        product.price = round(self.price * self.tax.tax_value)
        product.save()
        
        inventory = Inventory.objects.filter(
            product=self.product
        ).order_by('-id').first()
        
        if inventory:
            totalBal = inventory.total_balance_quantity + self.quantity
        else:
            totalBal = self.quantity
        
        Inventory.objects.create(
            product=self.product,
            sale_quantity = 0,
            purchase_quantity=self.quantity,
            total_balance_quantity=totalBal
        )
        
class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    #purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, default=0, null=True)
    #sale = models.ForeignKey(Bill, on_delete=models.CASCADE, default=0, null=True, blank=True)
    #vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True)
    purchase_quantity = models.FloatField(default=0, null=True)
    sale_quantity = models.FloatField(default=0, null=True)
    total_balance_quantity = models.FloatField(default=0)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = ("Inventory")
        verbose_name_plural = ("2. Inventario")

    def product_unit(self):
        return self.product.unit.title

    # def purchase_date(self):
    #     if self.purchase:
    #         return self.purchase.purchase_date
    '''
    def sale_date(self):
        if self.sale:
            return self.sale.sale_date
    '''
