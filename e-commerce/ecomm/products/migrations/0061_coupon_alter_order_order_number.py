# Generated by Django 5.0.6 on 2024-08-03 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0060_alter_order_order_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('discount', models.DecimalField(decimal_places=2, help_text='Discount percentage', max_digits=5)),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(default='690f0c15c59e4b7eaf56a31025c2343b', max_length=50, unique=True),
        ),
    ]
