# Generated by Django 5.0.7 on 2024-08-19 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cash_register', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='payment_method',
            field=models.CharField(choices=[('EFECTIVO', 'Efectivo'), ('TRANSFERECIA BANCARIA', 'Transferencia Bancaria'), ('TARJETA CREDITO', 'Tarjeta Credito'), ('NEQUI', 'Nequi'), ('OTROS', 'Otros')], default='EFECTIVO', max_length=50),
        ),
    ]
