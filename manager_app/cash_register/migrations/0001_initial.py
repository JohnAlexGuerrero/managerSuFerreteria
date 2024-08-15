# Generated by Django 5.0.7 on 2024-08-13 22:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sales', '0004_alter_bill_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_date', models.DateTimeField()),
                ('total', models.FloatField(default=0)),
                ('payment_method', models.CharField(choices=[('EFECTIVO', 'Cash'), ('TRANSFERECIA BANCARIA', 'Bank'), ('TARJETA CREDITO', 'Credit Card'), ('NEQUI', 'Nequi'), ('OTROS', 'Other')], default='EFECTIVO', max_length=50)),
                ('bill', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.bill')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            },
        ),
    ]
