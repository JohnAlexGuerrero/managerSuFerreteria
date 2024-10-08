# Generated by Django 5.0.7 on 2024-08-06 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inventory',
            options={'verbose_name': 'Inventory', 'verbose_name_plural': '1. Inventario'},
        ),
        migrations.AlterModelOptions(
            name='purchase',
            options={'verbose_name': 'Purchase', 'verbose_name_plural': '3. compras'},
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='sale_quantity',
        ),
        migrations.AddField(
            model_name='purchase',
            name='number_purchase',
            field=models.CharField(default='FV 4534', max_length=50, unique=True),
            preserve_default=False,
        ),
    ]
