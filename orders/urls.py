from django.urls import path
from . import views

urlpatterns = [
    path('confirm/', views.confirm_order_view, name='confirm_order'),
    path('place/', views.place_order, name='place_order'),
    path('my-orders/', views.order_list, name='order_list'),
    path('my-orders/', views.user_orders, name='user_orders'),
    path('my-orders/<int:order_id>/', views.order_detail, name='order_detail'),
]
