"""
Django settings for express_deals project.

Optimized for e-commerce platform with hardcoded development settings.
"""

import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-gm92zq*_*osw8xp6y5_zfy=@6!f)b9*-pfms&vmb0yiool99xn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '*.herokuapp.com',
    'express-deals-16b6c1fa4311.herokuapp.com'
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
    # 'channels',  # Temporarily disabled - causing import errors
    # 'notifications',  # Temporarily disabled due to Django 5.2 compatibility
    'django_celery_beat',
    'django_celery_results',
    
    # Local apps
    'products.apps.ProductsConfig',
    'orders.apps.OrdersConfig',
    'accounts.apps.AccountsConfig',
    'payments.apps.PaymentsConfig',
    'scraping.apps.ScrapingConfig',
    # 'realtime.apps.RealtimeConfig',  # Temporarily disabled - depends on channels
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
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

# Media files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Stripe Configuration (Development - use test keys)
STRIPE_PUBLIC_KEY = 'pk_test_development_key'
STRIPE_SECRET_KEY = 'sk_test_development_key'
STRIPE_WEBHOOK_SECRET = 'whsec_development_key'

# Email Configuration (Development - console backend)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

# Security Settings for Production
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Ensure logs directory exists
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

# Logging Configuration
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

# Celery Configuration
# Use Heroku Redis in production, local Redis in development
import os
redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
CELERY_BROKER_URL = redis_url
CELERY_RESULT_BACKEND = redis_url
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Only start Celery if Redis is available
CELERY_TASK_ALWAYS_EAGER = os.environ.get('CELERY_ALWAYS_EAGER', 'False').lower() == 'true'

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

# Third-party Service Configuration (Development - empty/disabled)
TWILIO_ACCOUNT_SID = ''
TWILIO_AUTH_TOKEN = ''

# WhatsApp Configuration (Development - hardcoded for development)
WHATSAPP_API_URL = 'https://api.whatsapp.com/send'
WHATSAPP_BUSINESS_API_URL = 'https://graph.facebook.com/v17.0'
WHATSAPP_ACCESS_TOKEN = ''  # Configure with your Facebook WhatsApp Business API token
WHATSAPP_PHONE_NUMBER_ID = ''  # Configure with your WhatsApp Business phone number ID
WHATSAPP_VERIFY_TOKEN = 'express_deals_whatsapp_webhook_dev'  # Verification token for development

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

# Email Configuration (Development - Console backend)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'  # Replace with actual email
EMAIL_HOST_PASSWORD = 'your-app-password'  # Replace with actual app password
DEFAULT_FROM_EMAIL = 'Express Deals <noreply@expressdeals.com>'

# SMS Configuration (Twilio) - Development
TWILIO_ACCOUNT_SID = 'your-twilio-account-sid'  # Replace with actual SID
TWILIO_AUTH_TOKEN = 'your-twilio-auth-token'   # Replace with actual token
TWILIO_PHONE_NUMBER = '+1234567890'  # Replace with actual Twilio number

# WhatsApp Configuration (Development)
WHATSAPP_ENABLED = True  # Enable WhatsApp notifications
WHATSAPP_ACCESS_TOKEN = 'your-whatsapp-access-token'  # Replace
WHATSAPP_PHONE_NUMBER_ID = 'your-phone-number-id'     # Replace
WHATSAPP_WEBHOOK_VERIFY_TOKEN = 'your-webhook-verify-token'  # Replace
WHATSAPP_RATE_LIMIT = 30  # Seconds between WhatsApp messages
WHATSAPP_MAX_RETRIES = 3  # Maximum retry attempts for failed messages

# SendGrid Configuration (Development - disabled)
SENDGRID_API_KEY = ''

# Sentry Configuration (Development - disabled)
SENTRY_DSN = ''
# Sentry is disabled in development - no initialization needed

# Site Configuration (Development)
SITE_URL = 'http://localhost:8000'
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

# Cache Configuration (Development - Redis local)
if os.environ.get('REDIS_URL'):
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': os.environ.get('REDIS_URL'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'CONNECTION_POOL_KWARGS': {
                    'max_connections': 10,
                    'retry_on_timeout': True,
                }
            }
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

# Session Configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE = 86400  # 24 hours
