#!/usr/bin/env python
"""
Express Deals - Environment Verification
Verify virtual environment setup and package installation
"""

import sys
import os

def verify_environment():
    """Verify the development environment setup"""
    print("🔍 EXPRESS DEALS - ENVIRONMENT VERIFICATION")
    print("=" * 60)
    
    # Check Python executable
    print("🐍 PYTHON ENVIRONMENT:")
    print(f"   Executable: {sys.executable}")
    
    # Check if virtual environment is active
    venv_active = (
        hasattr(sys, 'real_prefix') or 
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    )
    print(f"   Virtual Environment: {'✅ ACTIVE' if venv_active else '❌ NOT ACTIVE'}")
    print(f"   Python Version: {sys.version}")
    print()
    
    # Check critical packages
    print("📦 PACKAGE VERIFICATION:")
    
    packages_to_check = [
        ('django', 'Django Framework'),
        ('stripe', 'Stripe Payments'),
        ('requests', 'HTTP Library'),
        ('PIL', 'Image Processing'),
        ('twilio', 'SMS/Voice API'),
        ('redis', 'Redis Client'),
        ('celery', 'Background Tasks'),
    ]
    
    for package, description in packages_to_check:
        try:
            module = __import__(package)
            version = getattr(module, '__version__', getattr(module, 'VERSION', 'Unknown'))
            print(f"   ✅ {description}: {version}")
        except ImportError:
            print(f"   ❌ {description}: NOT INSTALLED")
    
    print()
    
    # Check Django setup
    print("🌐 DJANGO VERIFICATION:")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
        import django
        django.setup()
        from django.conf import settings
        
        print(f"   ✅ Django Settings: OK")
        print(f"   Debug Mode: {settings.DEBUG}")
        print(f"   Database: {settings.DATABASES['default']['ENGINE'].split('.')[-1]}")
        
        # Check Stripe configuration
        stripe_configured = (
            hasattr(settings, 'STRIPE_SECRET_KEY') and 
            settings.STRIPE_SECRET_KEY and
            'sk_test_' in settings.STRIPE_SECRET_KEY
        )
        print(f"   Stripe Configuration: {'✅ CONFIGURED' if stripe_configured else '❌ NOT CONFIGURED'}")
        
        if stripe_configured:
            print(f"   Stripe Key: {settings.STRIPE_SECRET_KEY[:20]}...")
            
    except Exception as e:
        print(f"   ❌ Django Setup Error: {e}")
    
    print()
    
    # Environment recommendations
    print("💡 RECOMMENDATIONS:")
    
    if not venv_active:
        print("   ⚠️ Activate virtual environment: .\.venv\Scripts\Activate.ps1")
    
    if venv_active:
        print("   ✅ Virtual environment is properly activated")
        print("   ✅ Packages are isolated from global Python")
        print("   ✅ Ready for development and testing")
    
    print("=" * 60)

if __name__ == "__main__":
    verify_environment()
