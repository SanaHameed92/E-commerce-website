# products/forms.py

from django import forms
from .models import Product, ProductImage

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title', 'description', 'category', 'original_price', 'rating', 'brand',
            'quantity', 'trending', 'product_image','availability_status','in_stock'
        ]
       

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']
