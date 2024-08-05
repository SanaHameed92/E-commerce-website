# Generated by Django 5.0.6 on 2024-08-04 05:40

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0083_remove_order_coupon_alter_order_order_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='grand_total',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(default='8c04373932644bab9d24d79ffdf05e76', max_length=50, unique=True),
        ),
    ]
