# Generated by Django 5.0.6 on 2024-08-05 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0094_alter_order_order_number_alter_product_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(default='092c6d0d3e8a4e6589db3181ca6deb47', max_length=50, unique=True),
        ),
    ]
