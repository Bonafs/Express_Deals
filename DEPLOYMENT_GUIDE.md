# Express Deals - Advanced Features Deployment Guide

## Overview
This guide covers the deployment and configuration of the advanced automation features added to Express Deals, including web scraping, price monitoring, real-time notifications, and background task processing.

## New Features Added

### 1. Web Scraping & Price Monitoring
- **Models**: ScrapeTarget, ScrapeJob, ScrapedProduct, PriceAlert, AlertNotification
- **Scrapers**: Support for requests, BeautifulSoup, Selenium, and Playwright
- **Price Tracking**: Automated price monitoring for products and external URLs
- **Alert System**: Email/SMS/Push notifications for price drops and stock changes

### 2. Real-time Features
- **WebSocket Support**: Live price updates and notifications via Django Channels
- **Live Dashboard**: Real-time admin dashboard for monitoring scraping activity
- **Push Notifications**: Browser push notifications for instant alerts

### 3. Background Task Processing
- **Celery Integration**: Asynchronous task processing for scraping and notifications
- **Scheduled Tasks**: Automated price checks, data cleanup, and trending analysis
- **Queue Management**: Separate queues for scraping, alerts, and notifications

### 4. User-facing Features
- **Alert Dashboard**: Comprehensive user interface for managing price alerts
- **Deal Discovery**: AI-powered deal discovery with filtering and search
- **Alert History**: Track savings and notification history
- **Preferences**: Customizable notification settings and quiet hours

## Dependencies Added

### Core Packages
```
# Web Scraping
scrapy==2.11.0
beautifulsoup4==4.12.2
requests==2.31.0
selenium==4.15.2
playwright==1.40.0
lxml==4.9.3

# Background Tasks
celery==5.3.4
redis==5.0.1
django-celery-beat==2.5.0
django-celery-results==2.6.0

# Real-time
channels==4.0.0
channels-redis==4.1.0
websockets==12.0

# Notifications
twilio==8.10.0
django-notifications-hq==1.8.3
webpush==0.3.0

# API & REST
djangorestframework==3.14.0
django-cors-headers==4.3.1

# Monitoring & Analytics
sentry-sdk==1.38.0
```

## Environment Configuration

### Required Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/express_deals

# Redis (for Celery and Channels)
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# Email Configuration
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your_sendgrid_api_key
SENDGRID_API_KEY=your_sendgrid_api_key

# SMS Configuration (Twilio)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# Web Push Notifications
VAPID_PRIVATE_KEY=your_vapid_private_key
VAPID_PUBLIC_KEY=your_vapid_public_key
VAPID_ADMIN_EMAIL=admin@yoursite.com

# Monitoring
SENTRY_DSN=your_sentry_dsn

# Scraping Configuration
SCRAPER_USER_AGENT=Express Deals Bot 1.0
SCRAPER_DELAY_MIN=1
SCRAPER_DELAY_MAX=5
PROXY_LIST=proxy1:port,proxy2:port

# Security
SECRET_KEY=your_secret_key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## Installation Steps

### 1. Install System Dependencies
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y redis-server postgresql postgresql-contrib python3-pip python3-venv

# Install Playwright browsers
playwright install

# Install Chrome for Selenium (if needed)
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
sudo apt update
sudo apt install -y google-chrome-stable
```

### 2. Install Python Dependencies
```bash
cd /path/to/express_deals
pip install -r requirements.txt
```

### 3. Database Migration
```bash
python manage.py makemigrations scraping realtime
python manage.py migrate
```

### 4. Create Superuser and Configure Admin
```bash
python manage.py createsuperuser
python manage.py collectstatic
```

### 5. Configure Redis
```bash
# Start Redis service
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Test Redis connection
redis-cli ping
```

## Service Configuration

### 1. Celery Worker Service
Create `/etc/systemd/system/express-deals-celery.service`:
```ini
[Unit]
Description=Express Deals Celery Worker
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/path/to/express_deals
Environment=DJANGO_SETTINGS_MODULE=express_deals.settings
ExecStart=/path/to/venv/bin/celery -A express_deals worker --loglevel=info --concurrency=4
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### 2. Celery Beat Service
Create `/etc/systemd/system/express-deals-celerybeat.service`:
```ini
[Unit]
Description=Express Deals Celery Beat
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/path/to/express_deals
Environment=DJANGO_SETTINGS_MODULE=express_deals.settings
ExecStart=/path/to/venv/bin/celery -A express_deals beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### 3. Django ASGI Service (for WebSockets)
Create `/etc/systemd/system/express-deals-asgi.service`:
```ini
[Unit]
Description=Express Deals ASGI
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/path/to/express_deals
Environment=DJANGO_SETTINGS_MODULE=express_deals.settings
ExecStart=/path/to/venv/bin/daphne -b 0.0.0.0 -p 8001 express_deals.asgi:application
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### 4. Enable and Start Services
```bash
sudo systemctl daemon-reload
sudo systemctl enable express-deals-celery
sudo systemctl enable express-deals-celerybeat
sudo systemctl enable express-deals-asgi
sudo systemctl start express-deals-celery
sudo systemctl start express-deals-celerybeat
sudo systemctl start express-deals-asgi
```

## Nginx Configuration

### WebSocket and ASGI Support
Add to your Nginx site configuration:
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Static files
    location /static/ {
        alias /path/to/express_deals/staticfiles/;
    }

    # Media files
    location /media/ {
        alias /path/to/express_deals/media/;
    }

    # WebSocket support
    location /ws/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Django application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Monitoring and Maintenance

### 1. Log Files
Monitor these log files:
- `/var/log/celery/express-deals-worker.log`
- `/var/log/celery/express-deals-beat.log`
- Django application logs
- Nginx access/error logs

### 2. Health Checks
Create monitoring scripts to check:
- Celery worker status: `celery -A express_deals inspect active`
- Redis connectivity: `redis-cli ping`
- Database connectivity
- WebSocket connections

### 3. Performance Monitoring
- Use Sentry for error tracking
- Monitor Celery task success/failure rates
- Track scraping success rates and response times
- Monitor notification delivery rates

### 4. Backup Strategy
- Regular database backups
- Backup configuration files
- Monitor disk space for logs and media files

## Testing the Installation

### 1. Test Celery
```bash
# Test basic Celery functionality
python manage.py shell
>>> from express_deals.celery import debug_task
>>> result = debug_task.delay()
>>> result.ready()
```

### 2. Test Scraping
```bash
# Create a scrape target via Django admin
# Then test scraping task
python manage.py shell
>>> from scraping.tasks import scrape_product
>>> scrape_product.delay(target_id=1)
```

### 3. Test Notifications
```bash
# Test email notification
python manage.py shell
>>> from scraping.tasks import send_email_notification
>>> send_email_notification.delay(user_id=1, subject="Test", message="Test message")
```

### 4. Test WebSockets
- Visit a product page as an authenticated user
- Open browser developer tools and check WebSocket connections
- Verify real-time price updates work

## Troubleshooting

### Common Issues

1. **Celery tasks not executing**
   - Check Redis connection
   - Verify Celery worker is running
   - Check task routing configuration

2. **WebSocket connections failing**
   - Verify ASGI service is running
   - Check Nginx WebSocket configuration
   - Confirm Channels Redis configuration

3. **Scraping failures**
   - Check for IP blocking (use proxies)
   - Verify user agent configuration
   - Monitor rate limiting

4. **Notification delivery issues**
   - Verify email/SMS service credentials
   - Check notification preferences
   - Monitor delivery logs

### Performance Optimization

1. **Database optimization**
   - Add indexes for frequently queried fields
   - Regular database maintenance
   - Consider read replicas for heavy read loads

2. **Caching**
   - Implement Redis caching for frequently accessed data
   - Cache product information and price history
   - Use CDN for static files

3. **Scaling**
   - Run multiple Celery workers
   - Use separate queues for different task types
   - Consider horizontal scaling with load balancers

## Security Considerations

1. **API Security**
   - Rate limiting for API endpoints
   - Authentication for all alert management
   - CSRF protection for forms

2. **Scraping Ethics**
   - Respect robots.txt files
   - Implement reasonable delays
   - Monitor and rotate IP addresses

3. **Data Protection**
   - Encrypt sensitive data
   - Regular security updates
   - Monitor for vulnerabilities

## Advanced Configuration

### Custom Scrapers
To add support for new websites, create custom scrapers in `scraping/scrapers.py`:

```python
def scrape_custom_site(url, **kwargs):
    """Custom scraper for specific website."""
    # Implementation here
    pass
```

### Custom Notification Channels
Extend the notification system by adding new channels in `scraping/notifications.py`:

```python
def send_custom_notification(user, message, **kwargs):
    """Send notification via custom channel."""
    # Implementation here
    pass
```

This deployment guide provides comprehensive instructions for setting up and running the advanced Express Deals features in a production environment.
