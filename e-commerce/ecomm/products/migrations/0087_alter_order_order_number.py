# Generated by Django 5.0.6 on 2024-08-04 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0086_alter_order_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(default='a3cf811fc10a46bdb7de484a56832f7c', max_length=50, unique=True),
        ),
    ]
