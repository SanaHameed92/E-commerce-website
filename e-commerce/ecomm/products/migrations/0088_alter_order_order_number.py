# Generated by Django 5.0.6 on 2024-08-04 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0087_alter_order_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(default='5770d7d45800416ba327c34034a12f28', max_length=50, unique=True),
        ),
    ]
