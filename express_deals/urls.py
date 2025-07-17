"""
URL configuration for express_deals project.
Optimized for e-commerce platform
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .health_views import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),  # Debug endpoint
    path('', include('products.urls')),
    path('accounts/', include('accounts.urls')),
    path('orders/', include('orders.urls')),
    path('payments/', include('payments.urls')),
    # path('alerts/', include('alerts.urls')),    # Temporarily disabled for deployment
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
