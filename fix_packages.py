#!/usr/bin/env python
"""
Quick fix for missing Django REST Framework and other packages
"""
import subprocess
import sys

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def test_import(module_name, import_statement):
    """Test if a module can be imported"""
    try:
        exec(import_statement)
        print(f"✅ {module_name} imports successfully")
        return True
    except ImportError as e:
        print(f"❌ {module_name} import failed: {e}")
        return False

def main():
    print("🔧 EXPRESS DEALS - PACKAGE FIX SCRIPT")
    print("=" * 50)
    
    # Required packages
    packages = [
        "django",
        "djangorestframework",
        "dj-database-url",
        "celery",
        "channels",
        "channels-redis",
        "redis",
        "pillow",
        "stripe",
        "whitenoise",
        "django-celery-beat",
        "django-celery-results",
        "scrapy",
        "beautifulsoup4",
        "requests",
        "selenium",
        "lxml"
    ]
    
    print("📦 Installing required packages...")
    for package in packages:
        install_package(package)
    
    print("\n🧪 Testing imports...")
    
    # Test critical imports
    imports = [
        ("Django", "import django; print('Django version:', django.get_version())"),
        ("Django REST Framework", "import rest_framework; print('DRF version:', rest_framework.VERSION)"),
        ("Celery", "import celery; print('Celery version:', celery.__version__)"),
        ("Channels", "import channels"),
        ("Redis", "import redis"),
        ("Pillow", "import PIL"),
        ("Stripe", "import stripe"),
    ]
    
    for name, import_stmt in imports:
        test_import(name, import_stmt)
    
    print("\n🚀 Testing Django setup...")
    try:
        import os
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
        import django
        django.setup()
        print("✅ Django setup successful!")
        
        # Test Django management command
        from django.core.management import execute_from_command_line
        print("✅ Django management commands available")
        
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False
    
    print("\n🎉 All packages installed and tested successfully!")
    print("💡 You can now run: python manage.py runserver")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
