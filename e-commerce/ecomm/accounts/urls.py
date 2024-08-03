from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/products/', views.admin_products, name='admin_products'),
    path('edit_product/<int:pk>/', views.edit_product, name='edit_product'),
    path('products/add/', views.add_product, name='add_product'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('category/<int:pk>/delete/', views.delete_category, name='delete_category'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/<int:user_id>/<str:scenario>/', views.verify_otp, name='verify_otp'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('admin/brands/toggle/<int:pk>/', views.toggle_brand_status, name='toggle_brand_status'),
    

  
]
