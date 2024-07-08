
from django.urls import path
from . import views

app_name = 'product_page'


    

app_name = 'product_page'

urlpatterns = [
    path('shop/',views.shop,name='shop'),
    path('shop-single/<int:product_id>/', views.shop_single, name='shop-single'),
    path('cart/',views.cart,name='cart'),

]