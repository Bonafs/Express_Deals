"""
Express Deals - Real-time WebSocket Routing
"""

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/notifications/', consumers.NotificationConsumer.as_asgi()),
    path('ws/product/<int:product_id>/', consumers.LivePriceConsumer.as_asgi()),
    path('ws/admin/', consumers.AdminDashboardConsumer.as_asgi()),
]
