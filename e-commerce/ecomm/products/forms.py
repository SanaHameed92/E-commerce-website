# products/forms.py

from django import forms
from .models import Product, ProductImage, Category, Brand, Size, Color

class ProductForm(forms.ModelForm):
    sizes = forms.ModelMultipleChoiceField(
        queryset=Size.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    colors = forms.ModelMultipleChoiceField(
        queryset=Color.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = Product
        fields = [
            'title', 'description', 'category', 'original_price', 'rating', 'brand',
            'quantity','max_qty_per_person', 'trending', 'product_image','availability_status','sizes','colors','featured',
            'popularity',
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
        

class CartUpdateForm(forms.Form):

    def __init__(self, *args, **kwargs):
        cart_items = kwargs.pop('cart_items', [])
        super().__init__(*args, **kwargs)
        for item in cart_items:
            self.fields[f'quantity_{item.id}'] = forms.IntegerField(
                initial=item.quantity,
                min_value=1,
                max_value=item.product.max_qty_per_person,
                label=item.product.title
            )

