from django.urls import path
from . import views


urlpatterns = [
    path('profile/',views.profile,name='profile'),
    path('personal_information/', views.personal_information, name='personal_information'),
    path('manage_address/', views.manage_address, name='manage_address'),
    path('add-address/', views.add_address, name='add_address'),
    path('edit-address/<int:address_id>/', views.edit_address, name='edit_address'),
    path('delete-address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order-detail/<uuid:order_number>/', views.order_detail, name='order_detail'),
     path('order/<uuid:order_number>/cancel/', views.cancel_order, name='cancel_order'),
    path('orders/', views.order_list, name='order_list'),
    path('update_order_status/', views.update_order_status, name='update_order_status')
]
