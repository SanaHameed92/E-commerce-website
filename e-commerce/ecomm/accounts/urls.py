from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('forgotPassword/',views.forgotPassword,name='forgotPassword')
]
