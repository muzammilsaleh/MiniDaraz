from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),  
    path('orders/', views.order_list, name='user_orders'),  
    path('add-address/', views.add_address, name='add_address'),  
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'), 


]
