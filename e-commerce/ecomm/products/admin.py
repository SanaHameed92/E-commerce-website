from django.contrib import admin

# Register your models here.
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'quantity', 'original_price', 'in_stock', 'trending', 'rating', 'created_at', 'updated_at')
    list_filter = ('category', 'in_stock', 'trending')
    search_fields = ('title', 'category__name')