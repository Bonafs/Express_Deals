from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('add-to-cart/<int:product_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('order-history/', views.OrderHistoryView.as_view(), name='order_history'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
]
