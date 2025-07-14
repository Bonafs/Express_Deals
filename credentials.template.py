# Express Deals - Secure Credentials File
# ==========================================
# This file contains sensitive information and should NEVER be committed to version control
# Copy this to 'credentials.py' and fill in your actual values

# Django Secret Key
SECRET_KEY = 'your-secret-key-here'

# Superuser Credentials
SUPERUSER_USERNAME = 'admin'
SUPERUSER_EMAIL = '527626@waes.ac.uk'
SUPERUSER_PASSWORD = 'Mobolaji'

# Database Credentials (if using local database)
DATABASE_NAME = 'express_deals_db'
DATABASE_USER = 'your-db-user'
DATABASE_PASSWORD = 'your-db-password'
DATABASE_HOST = 'localhost'
DATABASE_PORT = '5432'

# Email Configuration
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-email-password'

# Third-party API Keys
STRIPE_PUBLISHABLE_KEY = 'pk_test_your_stripe_key'
STRIPE_SECRET_KEY = 'sk_test_your_stripe_secret'

# Social Authentication Keys
GOOGLE_OAUTH2_KEY = 'your-google-oauth-key'
GOOGLE_OAUTH2_SECRET = 'your-google-oauth-secret'

# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'

# Sample Users (for development only)
SAMPLE_USERS = [
    {
        'username': 'testuser1',
        'email': 'testuser1@test.com',
        'first_name': 'Test',
        'last_name': 'User1',
        'password': 'testpassword123',
        'profile_data': {
            'phone': '+1234567890',
            'date_of_birth': '1990-01-15',
            'address': '123 Test St, Test City, TC 12345',
        }
    },
    {
        'username': 'testuser2',
        'email': 'testuser2@test.com',
        'first_name': 'Test',
        'last_name': 'User2',
        'password': 'testpassword456',
        'profile_data': {
            'phone': '+1234567891',
            'date_of_birth': '1985-05-22',
            'address': '456 Test Ave, Test City, TC 12346',
        }
    },
    {
        'username': 'bonafs',
        'email': 'bonafs@yahoo.com',
        'first_name': 'Bonafs',
        'last_name': '',
        'password': 'expressdeals',
        'profile_data': {
            'phone': '',
            'date_of_birth': '',
            'address': ''
        }
    }
]
