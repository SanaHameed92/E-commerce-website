# Generated by Django 5.0.6 on 2024-07-05 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_remove_product_product_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_image',
            field=models.ImageField(default='default_product_image.jpg', upload_to='photos/products', verbose_name='Product Image'),
        ),
        migrations.DeleteModel(
            name='ProductImage',
        ),
    ]
