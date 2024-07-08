
from django.urls import path
from . import views

app_name = 'main_page'

urlpatterns = [
    path('',views.index,name='index'),
    path('ex/',views.ex,name='ex'),
    #path('shop/',views.shop,name='shop'),
  
   
  
]
