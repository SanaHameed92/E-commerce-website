# Generated by Django 5.0.6 on 2024-08-03 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0066_cart_coupon_alter_order_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(default='fd124df6d63e4c2fb4f6bee888debc60', max_length=50, unique=True),
        ),
    ]
