
from django.urls import path
from . import views


    

app_name = 'product_page'

urlpatterns = [
    path('shop/',views.shop,name='shop'),
    path('shop-single/<int:product_id>/', views.shop_single, name='shop-single'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('product_filter_by_size/', views.product_filter_by_size, name='product_filter_by_size'),
    path('product_filter_by_color/', views.product_filter_by_color, name='product_filter_by_color'),
    path('checkout/',views.checkout,name='checkout')
    
    

]