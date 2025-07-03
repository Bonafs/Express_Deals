from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Cart URLs
    path('cart/', views.CartView.as_view(), name='cart'),
    path('add-to-cart/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('update-cart/', views.UpdateCartView.as_view(), name='update_cart'),
    path('remove-from-cart/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    
    # Checkout URLs
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    
    # Order URLs
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    
    # Wishlist URLs
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path('add-to-wishlist/', views.AddToWishlistView.as_view(), name='add_to_wishlist'),
    
    # Legacy URLs for backward compatibility
    path('order-history/', views.OrderHistoryView.as_view(), name='order_history'),
]
