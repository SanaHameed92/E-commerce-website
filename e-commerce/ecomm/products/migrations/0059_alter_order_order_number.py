# Generated by Django 5.0.6 on 2024-08-02 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0058_alter_order_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(default='7cf73795125a48cf8956fa46be8b09cf', max_length=50, unique=True),
        ),
    ]
