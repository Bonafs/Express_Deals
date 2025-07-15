from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('', views.ProductListView.as_view(), name='home'),  # Alias for backward compatibility
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:slug>/', views.CategoryListView.as_view(), name='category_list'),
    path('search/', views.search_products, name='search'),
    
    # URL Tracking API endpoints
    path('api/check-url-tracking/', views.check_url_tracking, name='check_url_tracking'),
    path('api/create-url-alert/', views.create_url_alert, name='create_url_alert'),
    path('api/user-tracking-stats/', views.get_user_tracking_stats, name='user_tracking_stats'),
]
