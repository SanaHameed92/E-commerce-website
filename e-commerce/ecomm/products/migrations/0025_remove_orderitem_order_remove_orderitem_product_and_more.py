# Generated by Django 5.0.6 on 2024-07-21 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0024_order_orderitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
