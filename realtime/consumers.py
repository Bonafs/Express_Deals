"""
Express Deals - WebSocket Consumers
Real-time notifications and live updates using Django Channels
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser
import logging

logger = logging.getLogger(__name__)


class NotificationConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time notifications
    """
    
    async def connect(self):
        """
        Accept WebSocket connection and join user group
        """
        # Get user from scope (set by auth middleware)
        self.user = self.scope["user"]
        
        if isinstance(self.user, AnonymousUser):
            # Reject anonymous users
            await self.close()
            return
        
        # Create group name for this user
        self.user_group_name = f"user_{self.user.id}"
        
        # Join user group
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send connection confirmation
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Connected to Express Deals notifications'
        }))
        
        logger.info(f"WebSocket connected for user {self.user.username}")
    
    async def disconnect(self, close_code):
        """
        Leave user group on disconnect
        """
        if hasattr(self, 'user_group_name'):
            await self.channel_layer.group_discard(
                self.user_group_name,
                self.channel_name
            )
        
        logger.info(f"WebSocket disconnected for user {getattr(self.user, 'username', 'unknown')}")
    
    async def receive(self, text_data):
        """
        Handle messages from WebSocket client
        """
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type', 'unknown')
            
            if message_type == 'ping':
                # Respond to ping with pong
                await self.send(text_data=json.dumps({
                    'type': 'pong',
                    'timestamp': text_data_json.get('timestamp')
                }))
            
            elif message_type == 'subscribe_product':
                # Subscribe to price updates for a specific product
                product_id = text_data_json.get('product_id')
                if product_id:
                    await self.subscribe_to_product(product_id)
            
            elif message_type == 'unsubscribe_product':
                # Unsubscribe from product updates
                product_id = text_data_json.get('product_id')
                if product_id:
                    await self.unsubscribe_from_product(product_id)
        
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))
    
    async def subscribe_to_product(self, product_id):
        """
        Subscribe to price updates for a specific product
        """
        product_group_name = f"product_{product_id}"
        
        await self.channel_layer.group_add(
            product_group_name,
            self.channel_name
        )
        
        await self.send(text_data=json.dumps({
            'type': 'subscription_confirmed',
            'product_id': product_id,
            'message': f'Subscribed to updates for product {product_id}'
        }))
    
    async def unsubscribe_from_product(self, product_id):
        """
        Unsubscribe from product updates
        """
        product_group_name = f"product_{product_id}"
        
        await self.channel_layer.group_discard(
            product_group_name,
            self.channel_name
        )
        
        await self.send(text_data=json.dumps({
            'type': 'subscription_cancelled',
            'product_id': product_id,
            'message': f'Unsubscribed from updates for product {product_id}'
        }))
    
    # Handlers for different types of notifications
    
    async def price_alert(self, event):
        """
        Send price alert notification to client
        """
        await self.send(text_data=json.dumps({
            'type': 'price_alert',
            'product_id': event['product_id'],
            'product_name': event['product_name'],
            'old_price': event['old_price'],
            'new_price': event['new_price'],
            'discount_percentage': event.get('discount_percentage'),
            'message': event['message'],
            'timestamp': event['timestamp']
        }))
    
    async def deal_alert(self, event):
        """
        Send deal alert notification to client
        """
        await self.send(text_data=json.dumps({
            'type': 'deal_alert',
            'deals': event['deals'],
            'message': event['message'],
            'timestamp': event['timestamp']
        }))
    
    async def scraping_update(self, event):
        """
        Send scraping progress update to client
        """
        await self.send(text_data=json.dumps({
            'type': 'scraping_update',
            'target_name': event['target_name'],
            'progress': event['progress'],
            'products_found': event['products_found'],
            'message': event['message'],
            'timestamp': event['timestamp']
        }))
    
    async def system_notification(self, event):
        """
        Send system notification to client
        """
        await self.send(text_data=json.dumps({
            'type': 'system_notification',
            'level': event.get('level', 'info'),
            'message': event['message'],
            'timestamp': event['timestamp']
        }))


class LivePriceConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for live price updates on product pages
    """
    
    async def connect(self):
        """
        Accept connection and join product group
        """
        self.product_id = self.scope['url_route']['kwargs']['product_id']
        self.product_group_name = f"product_{self.product_id}"
        
        # Join product group
        await self.channel_layer.group_add(
            self.product_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send current product price
        await self.send_current_price()
    
    async def disconnect(self, close_code):
        """
        Leave product group on disconnect
        """
        await self.channel_layer.group_discard(
            self.product_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """
        Handle client messages
        """
        try:
            data = json.loads(text_data)
            
            if data.get('type') == 'request_price':
                await self.send_current_price()
        
        except json.JSONDecodeError:
            pass
    
    async def send_current_price(self):
        """
        Send current product price to client
        """
        try:
            product = await self.get_product()
            if product:
                await self.send(text_data=json.dumps({
                    'type': 'price_update',
                    'product_id': self.product_id,
                    'price': str(product.price),
                    'stock_quantity': product.stock_quantity,
                    'is_available': product.is_active and product.stock_quantity > 0,
                    'timestamp': product.updated_at.isoformat() if product.updated_at else None
                }))
        except Exception as e:
            logger.error(f"Error sending current price for product {self.product_id}: {e}")
    
    @database_sync_to_async
    def get_product(self):
        """
        Get product from database
        """
        try:
            from products.models import Product
            return Product.objects.get(id=self.product_id)
        except Product.DoesNotExist:
            return None
    
    async def price_update(self, event):
        """
        Send price update to client
        """
        await self.send(text_data=json.dumps({
            'type': 'price_update',
            'product_id': event['product_id'],
            'price': event['price'],
            'old_price': event.get('old_price'),
            'stock_quantity': event.get('stock_quantity'),
            'is_available': event.get('is_available', True),
            'timestamp': event['timestamp']
        }))
    
    async def stock_update(self, event):
        """
        Send stock update to client
        """
        await self.send(text_data=json.dumps({
            'type': 'stock_update',
            'product_id': event['product_id'],
            'stock_quantity': event['stock_quantity'],
            'is_available': event['is_available'],
            'timestamp': event['timestamp']
        }))


class AdminDashboardConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for admin dashboard real-time updates
    """
    
    async def connect(self):
        """
        Accept connection for admin users only
        """
        self.user = self.scope["user"]
        
        # Check if user is admin
        if isinstance(self.user, AnonymousUser) or not self.user.is_staff:
            await self.close()
            return
        
        # Join admin group
        self.admin_group_name = "admin_dashboard"
        
        await self.channel_layer.group_add(
            self.admin_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        logger.info(f"Admin WebSocket connected for user {self.user.username}")
    
    async def disconnect(self, close_code):
        """
        Leave admin group on disconnect
        """
        if hasattr(self, 'admin_group_name'):
            await self.channel_layer.group_discard(
                self.admin_group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        """
        Handle admin commands
        """
        try:
            data = json.loads(text_data)
            command = data.get('command')
            
            if command == 'start_scraping':
                target_id = data.get('target_id')
                if target_id:
                    await self.start_scraping_task(target_id)
            
            elif command == 'get_scraping_status':
                await self.send_scraping_status()
        
        except json.JSONDecodeError:
            pass
    
    async def start_scraping_task(self, target_id):
        """
        Start a scraping task from admin dashboard
        """
        try:
            from scraping.tasks import scrape_target_task
            
            # Start the scraping task
            task = scrape_target_task.delay(target_id)
            
            await self.send(text_data=json.dumps({
                'type': 'task_started',
                'target_id': target_id,
                'task_id': task.id,
                'message': f'Scraping task started for target {target_id}'
            }))
        
        except Exception as e:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f'Failed to start scraping task: {str(e)}'
            }))
    
    async def send_scraping_status(self):
        """
        Send current scraping status to admin
        """
        try:
            status = await self.get_scraping_status()
            
            await self.send(text_data=json.dumps({
                'type': 'scraping_status',
                'active_jobs': status['active_jobs'],
                'recent_jobs': status['recent_jobs'],
                'total_products': status['total_products']
            }))
        
        except Exception as e:
            logger.error(f"Error getting scraping status: {e}")
    
    @database_sync_to_async
    def get_scraping_status(self):
        """
        Get current scraping status from database
        """
        from scraping.models import ScrapeJob, ScrapedProduct
        from django.utils import timezone
        from datetime import timedelta
        
        active_jobs = ScrapeJob.objects.filter(status='running').count()
        
        recent_jobs = list(ScrapeJob.objects.filter(
            started_at__gte=timezone.now() - timedelta(hours=24)
        ).values('id', 'status', 'target__name', 'products_found', 'started_at'))
        
        total_products = ScrapedProduct.objects.count()
        
        return {
            'active_jobs': active_jobs,
            'recent_jobs': recent_jobs,
            'total_products': total_products
        }
    
    # Admin notification handlers
    
    async def scraping_started(self, event):
        """
        Notify admin when scraping starts
        """
        await self.send(text_data=json.dumps({
            'type': 'scraping_started',
            'target_name': event['target_name'],
            'job_id': event['job_id'],
            'timestamp': event['timestamp']
        }))
    
    async def scraping_completed(self, event):
        """
        Notify admin when scraping completes
        """
        await self.send(text_data=json.dumps({
            'type': 'scraping_completed',
            'target_name': event['target_name'],
            'job_id': event['job_id'],
            'products_found': event['products_found'],
            'products_imported': event['products_imported'],
            'timestamp': event['timestamp']
        }))
    
    async def alert_triggered(self, event):
        """
        Notify admin when price alert is triggered
        """
        await self.send(text_data=json.dumps({
            'type': 'alert_triggered',
            'user_id': event['user_id'],
            'product_name': event['product_name'],
            'alert_type': event['alert_type'],
            'timestamp': event['timestamp']
        }))
