from django.urls import path
from . import views

app_name = 'alerts'

urlpatterns = [
    # Main dashboard
    path('', views.AlertsDashboardView.as_view(), name='dashboard'),
    
    # Alert management
    path('create/', views.CreateAlertView.as_view(), name='create_alert'),
    path('manage/<int:alert_id>/', views.ManageAlertView.as_view(),
         name='manage_alert'),
    path('product/<int:product_id>/', views.ProductAlertView.as_view(),
         name='product_alert'),
    
    # Settings and history
    path('settings/', views.AlertSettingsView.as_view(), name='settings'),
    path('history/', views.NotificationHistoryView.as_view(), name='history'),
]
