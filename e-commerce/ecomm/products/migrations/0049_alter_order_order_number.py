# Generated by Django 5.0.6 on 2024-08-02 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0048_alter_order_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(default='c0fc9147b63c4629b9657b2076ab9167', max_length=50, unique=True),
        ),
    ]
