# Generated by Django 5.0.6 on 2024-08-09 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0132_alter_order_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(default='a28421655fef4094bbac689bcc45ec40', max_length=50, unique=True),
        ),
    ]
