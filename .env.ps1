# Express Deals Environment Variables for PowerShell
# This file sets environment variables for local development

# Cloudinary Configuration
$env:CLOUDINARY_CLOUD_NAME = "dzecfjfju"
$env:CLOUDINARY_API_KEY = "853483899852935"
$env:CLOUDINARY_API_SECRET = "tFJ6Rb9xofDzV2Y1YrBZWaIZkhs"

# Django Configuration
$env:DEBUG = "True"
$env:SECRET_KEY = "express-deals-production-secret-key-2025-commercial-grade-security"
$env:DJANGO_SETTINGS_MODULE = "express_deals.settings"

# Database Configuration
$env:DATABASE_URL = "sqlite:///db.sqlite3"

# Commercial Scraping Configuration
$env:COMMERCIAL_SCRAPING_ENABLED = "True"
$env:ML_EXTRACTION_ENABLED = "True"
$env:PROXY_ROTATION_ENABLED = "True"
$env:MAX_CONCURRENT_SCRAPERS = "10"
$env:SCRAPING_RATE_LIMIT = "1"

# Redis Configuration (for commercial features)
$env:REDIS_URL = "redis://localhost:6379"

# Celery Configuration
$env:CELERY_BROKER_URL = "redis://localhost:6379"
$env:CELERY_RESULT_BACKEND = "redis://localhost:6379"

# Production Settings
$env:SECURE_SSL_REDIRECT = "False"
$env:SESSION_COOKIE_SECURE = "False"
$env:CSRF_COOKIE_SECURE = "False"

Write-Host "Express Deals environment variables loaded" -ForegroundColor Green
Write-Host "Commercial scraping system: CONFIGURED" -ForegroundColor Yellow
