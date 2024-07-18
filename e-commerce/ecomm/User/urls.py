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
]
