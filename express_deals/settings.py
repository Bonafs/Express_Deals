"""
Django settings for express_deals project.

Optimized for e-commerce platform with hardcoded development settings.
"""

import os
from pathlib import Path
import dj_database_url

# Import cloudinary settings for proper initialization
try:
    from . import cloudinary_settings  # noqa: F401
except ImportError:
    pass

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Generate a secure random key for production
import secrets
import string

def generate_secret_key():
    """Generate a cryptographically secure random secret key."""
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(alphabet) for i in range(64))

# Use environment variable or generate a strong random key
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    # Generate a strong default key for development
    SECRET_KEY = 'django-dev-' + generate_secret_key()

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG should NEVER be True in production - force False for Heroku
if 'DYNO' in os.environ:  # Running on Heroku
    DEBUG = False
else:
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.herokuapp.com',
    'express-deals-16b6c1fa4311.herokuapp.com'
]

# CSRF trusted origins for Heroku
CSRF_TRUSTED_ORIGINS = [
    'https://express-deals-16b6c1fa4311.herokuapp.com',
    'https://*.herokuapp.com',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    # 'django_celery_beat',        # REMOVED - Not needed for basic operation
    # 'django_celery_results',     # REMOVED - Not needed for basic operation
    
    # Local apps
    'products.apps.ProductsConfig',
    'orders.apps.OrdersConfig',
    'accounts.apps.AccountsConfig',
    'payments.apps.PaymentsConfig',
    # 'alerts.apps.AlertsConfig',  # Temporarily disabled due to null bytes issue

    # 'scraping.apps.ScrapingConfig',  # Temporarily disabled
    # 'realtime.apps.RealtimeConfig',  # Temporarily disabled - depends on channels
    # 'cloudinary',  # Temporarily disabled - module not available
    # 'cloudinary_storage',  # Temporarily disabled - module not available
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # Re-enabled CSRF middleware
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'express_deals.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'express_deals.context_processors.cart_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'express_deals.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Development database (SQLite) - hardcoded configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Production database (PostgreSQL) - Heroku configuration
if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.parse(
        os.environ.get('DATABASE_URL')
    )
    DATABASES['default']['CONN_MAX_AGE'] = 60
    DATABASES['default']['OPTIONS'] = {
        'MAX_CONNS': 20
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# WhiteNoise static files storage for production - disable manifest for debugging
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# WhiteNoise configuration for proper MIME types
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True

# MIME types will be configured by WhiteNoise automatically
# No global mimetypes configuration needed

# Media files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Cloudinary media storage - disabled for now
# CLOUDINARY_STORAGE = {
#     'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
#     'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
#     'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
# }
# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Stripe Configuration
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY', 'pk_test_placeholder_key')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_placeholder_key')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET', 'whsec_placeholder_key')

# Email Configuration
# Development: Console backend for testing
# Production: SMTP backend with Yahoo Mail
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = 'Express Deals <noreply@expressdeals.com>'
else:
    # Production email configuration with Yahoo Mail
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.mail.yahoo.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
    DEFAULT_FROM_EMAIL = os.environ.get(
        'DEFAULT_FROM_EMAIL', 
        'Express Deals <noreply@expressdeals.com>'
    )

# Security Settings for Production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_PRELOAD = True

# Force HTTPS and secure cookies in production
IS_PRODUCTION = not DEBUG or 'DYNO' in os.environ

if IS_PRODUCTION:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
else:
    # Development settings
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Ensure logs directory exists
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

# Logging Configuration
# Use Django's default logging configuration with our custom settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'payments': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Task Queue Configuration - DISABLED
# Background tasks will run synchronously without Redis/Celery
# This ensures Heroku doesn't try to connect to Redis services

# All background tasks disabled - run synchronously for stability
USE_ASYNC_TASKS = False

# Channels Configuration - Temporarily disabled
# ASGI_APPLICATION = 'express_deals.asgi.application'
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379/1')],
#         },
#     },
# }

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

# Notification Services Configuration
# Twilio SMS Configuration
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER', '')

# WhatsApp Configuration (Meta Business API)
WHATSAPP_API_URL = 'https://api.whatsapp.com/send'
WHATSAPP_BUSINESS_API_URL = 'https://graph.facebook.com/v18.0'
WHATSAPP_ACCESS_TOKEN = os.environ.get('WHATSAPP_ACCESS_TOKEN', '')
WHATSAPP_PHONE_NUMBER_ID = os.environ.get('WHATSAPP_PHONE_NUMBER_ID', '')
WHATSAPP_VERIFY_TOKEN = os.environ.get('WHATSAPP_VERIFY_TOKEN', 'express_deals_whatsapp_webhook_dev')

# WhatsApp Template Configuration (Hardcoded for development)
WHATSAPP_TEMPLATES = {
    'price_alert': {
        'name': 'price_alert_template',
        'language': 'en',
        'category': 'MARKETING'
    },
    'deal_notification': {
        'name': 'deal_notification_template', 
        'language': 'en',
        'category': 'MARKETING'
    },
    'order_confirmation': {
        'name': 'order_confirmation_template',
        'language': 'en', 
        'category': 'TRANSACTIONAL'
    }
}

# Additional Service Configuration
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', '')
SENTRY_DSN = os.environ.get('SENTRY_DSN', '')

# Site Configuration
SITE_URL = os.environ.get('SITE_URL', 'http://localhost:8000')
SITE_NAME = 'Express Deals'

# Web Scraping Configuration
SCRAPING_USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
]

SCRAPING_RATE_LIMIT = 1  # Seconds between requests
SCRAPING_MAX_RETRIES = 3
SCRAPING_TIMEOUT = 30  # Seconds

# Chrome/Selenium Configuration (Development)
CHROME_DRIVER_PATH = None  # Use system PATH
SELENIUM_HEADLESS = True

# Price Alert Configuration
MAX_ALERTS_PER_USER = 50
ALERT_CHECK_FREQUENCY = 30  # Minutes
PRICE_CHANGE_THRESHOLD = 0.01  # Minimum price change to trigger alert

# File Upload Configuration
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

# Cache Configuration - Database only (no Redis dependency)
# Use stable database caching instead of Redis for reliability
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
            'CULL_PERCENTAGE': 25,
        }
    }
}

# Session Configuration (Database sessions for stability, Redis for caching)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Keep sessions in PostgreSQL
SESSION_COOKIE_AGE = 86400  # 24 hours
# Do not use SESSION_CACHE_ALIAS to avoid Redis/PostgreSQL conflicts

# User Agent Configuration for Web Scraping
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
]

# Note: Django will automatically initialize logging using the LOGGING setting
# No need to manually call logging.config.dictConfig(LOGGING) here
