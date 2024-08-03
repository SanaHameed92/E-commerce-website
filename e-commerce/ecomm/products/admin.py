from datetime import timezone
from django.contrib import admin

# Register your models here.
from .models import Coupon, Product, Category, Brand, Size, Color, ProductImage,Order,OrderItem

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(ProductImage)
admin.site.register(Order)
admin.site.register(OrderItem)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'quantity', 'original_price', 'in_stock', 'trending', 'rating', 'created_at', 'updated_at')
    list_filter = ('category', 'in_stock', 'trending')
    search_fields = ('title', 'category__name')

    

class CouponAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'discount', 'valid_from', 'valid_to', 'status')
    list_filter = ('status', 'valid_from', 'valid_to')
    search_fields = ('name', 'code')
    ordering = ('-valid_to',)  # Order by expiration date in descending order

    def save_model(self, request, obj, form, change):
        # Automatically set the status before saving
        today = timezone.now().date()
        if obj.valid_from <= today <= obj.valid_to:
            obj.status = 'active'
        elif today < obj.valid_from:
            obj.status = 'inactive'
        else:
            obj.status = 'expired'
        super().save_model(request, obj, form, change)

    def get_actions(self, request):
        actions = super().get_actions(request)
        # Optionally remove some actions or add custom actions here
        return actions

admin.site.register(Coupon, CouponAdmin)