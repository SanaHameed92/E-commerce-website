# Generated by Django 5.0.6 on 2024-08-03 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0076_order_payment_id_alter_order_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(default='6006a2e6be464667bf3fe87936dea346', max_length=50, unique=True),
        ),
    ]
