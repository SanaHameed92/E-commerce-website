
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name

class Brand(models.Model):
    brand_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='brands', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.brand_name
    
class Size(models.Model):
    size_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.size_name
    
class Color(models.Model):
    color_name = models.CharField(max_length=50, unique=True)
    color_code = models.CharField(max_length=10)  # Assuming you store color code as a string

    def __str__(self):
        return self.color_name
    

class Product(models.Model):
    AVAILABILITY_CHOICES = [
        ('in_stock', _('In Stock')),
        ('sold_out', _('Sold Out')),
    ]

    title = models.CharField(max_length=100)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    max_qty_per_person = models.PositiveIntegerField(default=2)
    in_stock = models.PositiveIntegerField(default=1)
    availability_status = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='in_stock')
    trending = models.BooleanField(default=False, help_text=_('0=default, 1=Hidden'))
    rating = models.PositiveIntegerField(default=0, help_text=_('Rating from 1 to 5'), validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ])
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='product_creator', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    product_image = models.ImageField(upload_to='photos/products', verbose_name=_("Product Image"), default='default_product_image.jpg')
    featured = models.BooleanField(default=False, help_text=_('Is this product featured?'))
    popularity = models.IntegerField(default=0)
    sizes = models.ManyToManyField(Size, blank=True)
    colors = models.ManyToManyField(Color, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def main_image(self):
        return self.product_image.url if self.product_image else None



class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/products')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image of {self.product.title}"
    

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.product.original_price * self.quantity
    


