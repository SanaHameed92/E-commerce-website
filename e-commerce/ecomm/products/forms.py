# products/forms.py

from django import forms
from .models import Product, ProductImage, Category, Brand, Size, Color

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title', 'description', 'category', 'original_price', 'rating', 'brand',
            'quantity', 'trending', 'product_image','availability_status','in_stock'
        ]



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name','is_active']

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['brand_name','category','is_active']

class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = ['size_name']

class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = ['color_name']



class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']
