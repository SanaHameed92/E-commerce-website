# Generated by Django 5.0.6 on 2024-08-05 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0114_alter_order_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(default='2c45f0d7a0f944e28204cb93563a4acd', max_length=50, unique=True),
        ),
    ]
