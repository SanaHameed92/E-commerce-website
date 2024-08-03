# Generated by Django 5.0.6 on 2024-08-03 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0070_cartitem_added_at_alter_cartitem_cart_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='added_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(default='70ffa62a90f54699be83db53c1d10891', max_length=50, unique=True),
        ),
    ]
