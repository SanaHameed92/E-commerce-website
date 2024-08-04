# Generated by Django 5.0.6 on 2024-08-04 05:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0081_remove_order_paid_by_razorpay_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='grand_total',
        ),
        migrations.AddField(
            model_name='order',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.coupon'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(default='eb800fb6659841eb8c128462df2b86ca', max_length=50, unique=True),
        ),
    ]
