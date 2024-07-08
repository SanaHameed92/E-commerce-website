from django.db import models
from django.utils import timezone
from django.conf import settings
from category.models import Category
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

class Product(models.Model):
    AVAILABILITY_CHOICES = [
        ('in_stock', _('In Stock')),
        ('sold_out', _('Sold Out')),
    ]

    title = models.CharField(max_length=100)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField()
    in_stock = models.BooleanField(default=True)
    availability_status = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='in_stock')
    trending = models.BooleanField(default=False, help_text=_('0=default, 1=Hidden'))
    rating = models.IntegerField(default=0, help_text=_('Rating from 1 to 5'), validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ])
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='product_creator', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    product_image = models.ImageField(upload_to='photos/products', verbose_name=_("Product Image"), default='default_product_image.jpg')
    featured = models.BooleanField(default=False, help_text=_('Is this product featured?'))
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def main_image(self):
        return self.product_image.url if self.product_image else None
