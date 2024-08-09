from django.urls import path
from . import views

urlpatterns = [
    path('my-wallet/', views.my_wallet, name='my_wallet'),
    path('order/<str:order_number>/request-return/', views.request_return, name='request_return'),
    path('admin/return-requests/', views.admin_return_requests, name='admin_return_requests'),
    path('admin/return-request/<int:return_request_id>/confirm/', views.admin_confirm_return, name='admin_confirm_return'),
    path('admin/return-request/<int:return_request_id>/reject/', views.admin_reject_return, name='admin_reject_return'),
    path('referral/', views.referral_page, name='referral'),
]
