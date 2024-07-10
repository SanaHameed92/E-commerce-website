from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('products/', views.admin_products, name='admin_products'),
    path('edit_product/<int:pk>/', views.edit_product, name='edit_product'),
    path('products/add/', views.add_product, name='add_product'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('category/<int:pk>/delete/', views.delete_category, name='delete_category'),
    path('forgotPassword/',views.forgotPassword,name='forgotPassword')
]
