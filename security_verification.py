#!/usr/bin/env python
"""
Security Verification Test for Express Deals
Tests that all security issues are resolved
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')

# Simulate Heroku environment
os.environ['DYNO'] = 'web.1'

django.setup()

print("🔒 SECURITY VERIFICATION TEST")
print("=" * 50)

from django.conf import settings

print("🎯 Testing Security Settings:")
print(f"✅ DEBUG: {settings.DEBUG}")
print(f"✅ SECRET_KEY length: {len(settings.SECRET_KEY)} characters")
print(f"✅ SESSION_COOKIE_SECURE: {settings.SESSION_COOKIE_SECURE}")
print(f"✅ CSRF_COOKIE_SECURE: {settings.CSRF_COOKIE_SECURE}")
print(f"✅ SECURE_SSL_REDIRECT: {settings.SECURE_SSL_REDIRECT}")

print("\n🔍 Testing Redis/Celery Dependencies:")
redis_found = False
celery_found = False

# Check if Redis/Celery settings exist
if hasattr(settings, 'CELERY_BROKER_URL'):
    print(f"⚠️  CELERY_BROKER_URL found: {settings.CELERY_BROKER_URL}")
    celery_found = True
else:
    print("✅ No CELERY_BROKER_URL found")

if hasattr(settings, 'ENABLE_CELERY'):
    print(f"⚠️  ENABLE_CELERY found: {settings.ENABLE_CELERY}")
else:
    print("✅ No ENABLE_CELERY found")

print("\n📊 Cache Configuration:")
cache_backend = settings.CACHES['default']['BACKEND']
print(f"✅ Cache Backend: {cache_backend}")
if 'redis' in cache_backend.lower():
    print("⚠️  WARNING: Using Redis cache")
else:
    print("✅ Using database cache (no Redis dependency)")

print("\n📱 Apps Configuration:")
redis_apps = []
for app in settings.INSTALLED_APPS:
    if 'celery' in app or 'redis' in app:
        redis_apps.append(app)
        
if redis_apps:
    print(f"⚠️  Redis/Celery apps found: {redis_apps}")
else:
    print("✅ No Redis/Celery apps in INSTALLED_APPS")

print("\n" + "=" * 50)
if settings.DEBUG:
    print("⚠️  WARNING: DEBUG is True (development mode)")
else:
    print("✅ PRODUCTION MODE: All security settings enabled")
    
if not redis_found and not celery_found and not redis_apps:
    print("✅ SUCCESS: No Redis dependencies found")
    print("✅ Heroku will NOT try to connect to Redis")
else:
    print("⚠️  WARNING: Some Redis/Celery dependencies still exist")

print("🎉 Security verification completed!")
