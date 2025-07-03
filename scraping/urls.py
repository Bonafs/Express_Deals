"""
Express Deals - Scraping URLs
URL configuration for alert management and scraping features
"""

from django.urls import path
from . import views

app_name = 'alerts'

urlpatterns = [
    # Alert Dashboard
    path('', views.alert_dashboard, name='dashboard'),
    path('create/', views.create_alert, name='create'),
    path('create/<int:product_id>/', views.create_alert, name='create_for_product'),
    
    # Alert Management
    path('toggle/<int:alert_id>/', views.toggle_alert, name='toggle'),
    path('delete/<int:alert_id>/', views.delete_alert, name='delete'),
    
    # Alert History and Preferences
    path('history/', views.alert_history, name='history'),
    path('preferences/', views.alert_preferences, name='preferences'),
    
    # Deal Discovery
    path('deals/', views.discover_deals, name='discover_deals'),
    
    # API Endpoints
    path('api/count/', views.api_alert_count, name='api_count'),
    path('api/deals/', views.api_recent_deals, name='api_deals'),
    path('api/quick-alert/', views.api_create_quick_alert, name='api_quick_alert'),
]
