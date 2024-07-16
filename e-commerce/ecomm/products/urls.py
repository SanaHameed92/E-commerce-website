
from django.urls import path
from . import views


    

app_name = 'product_page'

urlpatterns = [
    path('shop/',views.shop,name='shop'),
    path('shop-single/<int:product_id>/', views.shop_single, name='shop-single'),
    path('cart/',views.cart,name='cart'),
    path('product_filter_by_size/', views.product_filter_by_size, name='product_filter_by_size'),
    path('product_filter_by_color/', views.product_filter_by_color, name='product_filter_by_color'),
    
    

]