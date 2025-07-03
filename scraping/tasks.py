"""
Express Deals - Background Tasks
Celery tasks for web scraping, price monitoring, and notifications
"""

from celery import shared_task
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import logging
from datetime import timedelta

from .models import ScrapeTarget, ScrapeJob, PriceAlert, AlertNotification, ScrapedProduct
from .scrapers import ProductScraper
from .notifications import NotificationService
from products.models import Product

logger = logging.getLogger(__name__)


@shared_task
def scrape_target_task(target_id, search_query='', max_pages=None):
    """
    Background task to scrape a specific target
    """
    try:
        target = ScrapeTarget.objects.get(id=target_id, status='active')
        scraper = ProductScraper()
        job = scraper.scrape_target(target, search_query, max_pages)
        
        logger.info(f"Scraping task completed for {target.name}: {job.products_found} products found")
        return {
            'target_id': target_id,
            'job_id': job.id,
            'products_found': job.products_found,
            'products_imported': job.products_imported,
            'status': job.status
        }
    
    except ScrapeTarget.DoesNotExist:
        logger.error(f"ScrapeTarget {target_id} not found")
        return {'error': 'Target not found'}
    
    except Exception as e:
        logger.error(f"Scraping task failed for target {target_id}: {e}")
        return {'error': str(e)}


@shared_task
def scrape_all_active_targets():
    """
    Periodic task to scrape all active targets
    """
    active_targets = ScrapeTarget.objects.filter(status='active')
    results = []
    
    for target in active_targets:
        # Check if enough time has passed since last scrape
        if target.last_scraped:
            hours_since_scrape = (timezone.now() - target.last_scraped).total_seconds() / 3600
            if hours_since_scrape < target.scrape_frequency_hours:
                continue
        
        # Start scraping task
        result = scrape_target_task.delay(target.id)
        results.append({
            'target_id': target.id,
            'target_name': target.name,
            'task_id': result.id
        })
    
    logger.info(f"Started scraping for {len(results)} targets")
    return results


@shared_task
def check_price_alerts():
    """
    Check all active price alerts and trigger notifications
    """
    active_alerts = PriceAlert.objects.filter(status='active')
    triggered_alerts = 0
    
    for alert in active_alerts:
        try:
            if alert.product:
                # Check specific product alert
                if check_product_alert(alert):
                    triggered_alerts += 1
            elif alert.search_keywords:
                # Check keyword-based alert
                if check_keyword_alert(alert):
                    triggered_alerts += 1
        
        except Exception as e:
            logger.error(f"Error checking alert {alert.id}: {e}")
    
    logger.info(f"Price alert check completed: {triggered_alerts} alerts triggered")
    return {'checked': active_alerts.count(), 'triggered': triggered_alerts}


def check_product_alert(alert):
    """
    Check if a specific product alert should be triggered
    """
    product = alert.product
    current_price = product.price
    
    should_trigger = False
    
    if alert.alert_type == 'below' and alert.target_price:
        should_trigger = current_price <= alert.target_price
    
    elif alert.alert_type == 'above' and alert.target_price:
        should_trigger = current_price >= alert.target_price
    
    elif alert.alert_type == 'percentage' and alert.percentage_threshold:
        # Check recent scraped products for price drops
        recent_scraped = ScrapedProduct.objects.filter(
            imported_product=product,
            scraped_at__gte=timezone.now() - timedelta(hours=24)
        ).order_by('-scraped_at').first()
        
        if recent_scraped and recent_scraped.original_price:
            discount = recent_scraped.discount_percentage
            should_trigger = discount >= alert.percentage_threshold
    
    if should_trigger:
        trigger_alert(alert, product, current_price)
        return True
    
    return False


def check_keyword_alert(alert):
    """
    Check keyword-based alerts against recent scraped products
    """
    keywords = alert.search_keywords.lower().split()
    
    # Find recent products matching keywords
    recent_products = ScrapedProduct.objects.filter(
        scraped_at__gte=timezone.now() - timedelta(hours=24),
        is_processed=True
    )
    
    triggered = False
    
    for product in recent_products:
        title_lower = product.title.lower()
        
        # Check if all keywords match
        if all(keyword in title_lower for keyword in keywords):
            
            should_trigger = False
            
            if alert.alert_type == 'below' and alert.target_price:
                should_trigger = product.price <= alert.target_price
            
            elif alert.alert_type == 'percentage' and alert.percentage_threshold:
                should_trigger = product.discount_percentage >= alert.percentage_threshold
            
            elif alert.alert_type == 'deal':
                # Trigger for significant discounts or low prices
                should_trigger = product.discount_percentage >= 20 or product.price <= 50
            
            if should_trigger:
                trigger_alert(alert, product.imported_product, product.price)
                triggered = True
    
    return triggered


def trigger_alert(alert, product, price):
    """
    Trigger an alert and send notifications
    """
    try:
        alert.status = 'triggered'
        alert.last_triggered = timezone.now()
        alert.save()
        
        # Send notifications
        notification_service = NotificationService()
        
        message = f"🚨 PRICE ALERT: {product.name} is now ${price}"
        if hasattr(product, 'discount_percentage'):
            message += f" ({product.discount_percentage}% off!)"
        
        # Email notification
        if alert.email_enabled and alert.user.email:
            send_email_alert.delay(alert.user.id, alert.id, message, product.id)
        
        # SMS notification
        if alert.sms_enabled and hasattr(alert.user, 'profile') and alert.user.profile.phone_number:
            send_sms_alert.delay(alert.user.id, alert.id, message)
        
        # Push notification
        if alert.push_enabled:
            send_push_notification.delay(alert.user.id, alert.id, message)
        
        logger.info(f"Alert {alert.id} triggered for user {alert.user.username}")
    
    except Exception as e:
        logger.error(f"Error triggering alert {alert.id}: {e}")


@shared_task
def send_email_alert(user_id, alert_id, message, product_id):
    """
    Send email alert notification
    """
    try:
        user = User.objects.get(id=user_id)
        alert = PriceAlert.objects.get(id=alert_id)
        product = Product.objects.get(id=product_id)
        
        subject = f"Express Deals Alert: {product.name}"
        
        html_message = f"""
        <html>
        <body>
            <h2>🚨 Price Alert Triggered!</h2>
            <p>{message}</p>
            <div style="border: 1px solid #ddd; padding: 15px; margin: 10px 0;">
                <h3>{product.name}</h3>
                <p><strong>Current Price: ${product.price}</strong></p>
                <p>{product.description}</p>
                <a href="{settings.SITE_URL}/products/{product.id}/" 
                   style="background: #007bff; color: white; padding: 10px 20px; text-decoration: none;">
                   View Product
                </a>
            </div>
            <p>Don't miss this deal! Visit Express Deals now.</p>
        </body>
        </html>
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        # Record notification
        AlertNotification.objects.create(
            alert=alert,
            channel='email',
            status='sent',
            message=message,
            recipient=user.email,
            delivered_at=timezone.now()
        )
        
        logger.info(f"Email alert sent to {user.email}")
        return True
    
    except Exception as e:
        logger.error(f"Failed to send email alert: {e}")
        # Record failed notification
        AlertNotification.objects.create(
            alert_id=alert_id,
            channel='email',
            status='failed',
            message=message,
            recipient=user.email if 'user' in locals() else 'unknown',
            error_message=str(e)
        )
        return False


@shared_task
def send_sms_alert(user_id, alert_id, message):
    """
    Send SMS alert notification using Twilio
    """
    try:
        from twilio.rest import Client
        
        user = User.objects.get(id=user_id)
        alert = PriceAlert.objects.get(id=alert_id)
        
        # Get phone number from user profile
        phone_number = getattr(user.profile, 'phone_number', None)
        if not phone_number:
            raise ValueError("User has no phone number")
        
        # Initialize Twilio client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
        # Send SMS
        twilio_message = client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        
        # Record notification
        AlertNotification.objects.create(
            alert=alert,
            channel='sms',
            status='sent',
            message=message,
            recipient=phone_number,
            delivered_at=timezone.now()
        )
        
        logger.info(f"SMS alert sent to {phone_number}")
        return True
    
    except Exception as e:
        logger.error(f"Failed to send SMS alert: {e}")
        # Record failed notification
        AlertNotification.objects.create(
            alert_id=alert_id,
            channel='sms',
            status='failed',
            message=message,
            recipient=phone_number if 'phone_number' in locals() else 'unknown',
            error_message=str(e)
        )
        return False


@shared_task
def send_push_notification(user_id, alert_id, message):
    """
    Send push notification (placeholder for future implementation)
    """
    try:
        user = User.objects.get(id=user_id)
        alert = PriceAlert.objects.get(id=alert_id)
        
        # TODO: Implement actual push notification service
        # For now, just record the attempt
        
        AlertNotification.objects.create(
            alert=alert,
            channel='push',
            status='sent',
            message=message,
            recipient=f"user_{user.id}",
            delivered_at=timezone.now()
        )
        
        logger.info(f"Push notification sent to user {user.id}")
        return True
    
    except Exception as e:
        logger.error(f"Failed to send push notification: {e}")
        return False


@shared_task
def cleanup_old_data():
    """
    Clean up old scraping data and notifications
    """
    cutoff_date = timezone.now() - timedelta(days=30)
    
    # Delete old scrape jobs and related data
    old_jobs = ScrapeJob.objects.filter(completed_at__lt=cutoff_date)
    jobs_deleted = old_jobs.count()
    old_jobs.delete()
    
    # Delete old notifications
    old_notifications = AlertNotification.objects.filter(sent_at__lt=cutoff_date)
    notifications_deleted = old_notifications.count()
    old_notifications.delete()
    
    logger.info(f"Cleanup completed: {jobs_deleted} jobs, {notifications_deleted} notifications deleted")
    return {'jobs_deleted': jobs_deleted, 'notifications_deleted': notifications_deleted}


@shared_task
def import_scraped_products():
    """
    Process unprocessed scraped products and import them to catalog
    """
    unprocessed = ScrapedProduct.objects.filter(is_processed=False)[:100]  # Process in batches
    
    scraper = ProductScraper()
    imported_count = 0
    
    for scraped_product in unprocessed:
        if scraper.import_to_catalog(scraped_product):
            imported_count += 1
    
    logger.info(f"Imported {imported_count} scraped products")
    return {'processed': len(unprocessed), 'imported': imported_count}
