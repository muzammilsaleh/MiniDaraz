from django.urls import path
from . import views

urlpatterns = [
    path('place/', views.place_order, name='place_order'),
    path('my/', views.order_list, name='order_list'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
]
