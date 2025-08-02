from django.urls import path
from . import views

app_name = 'pharmacy'

urlpatterns = [
    path('store/', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders, name='orders'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('api/cart/add/', views.api_add_to_cart, name='api_add_to_cart'),
    path('api/cart/remove/', views.api_remove_from_cart, name='api_remove_from_cart'),
    path('api/cart/update/', views.api_update_cart, name='api_update_cart'),
    path('api/checkout/', views.api_checkout, name='api_checkout'),
]