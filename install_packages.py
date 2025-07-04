#!/usr/bin/env python
"""
Express Deals Package Installer - Handles subprocess issues
"""
import sys
import subprocess
import os

def install_package(package_name):
    """Install a package using pip with proper error handling"""
    print(f"📦 Installing {package_name}...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", package_name
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ Successfully installed {package_name}")
            return True
        else:
            print(f"❌ Failed to install {package_name}")
            print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ Installation of {package_name} timed out")
        return False
    except Exception as e:
        print(f"❌ Installation of {package_name} failed: {e}")
        return False

def main():
    print("🔧 EXPRESS DEALS - PACKAGE INSTALLER")
    print("=" * 50)
    
    # Critical packages for Express Deals
    critical_packages = [
        "django",
        "djangorestframework",
        "channels",
        "channels-redis",
        "dj-database-url",
        "whitenoise",
        "pillow",
        "stripe",
        "celery",
        "redis",
        "django-celery-beat",
        "django-celery-results"
    ]
    
    # Install critical packages first
    print("\n🎯 Installing critical packages...")
    success_count = 0
    
    for package in critical_packages:
        if install_package(package):
            success_count += 1
    
    print(f"\n📊 Installation Summary:")
    print(f"✅ Successful: {success_count}/{len(critical_packages)}")
    print(f"❌ Failed: {len(critical_packages) - success_count}/{len(critical_packages)}")
    
    # Test critical imports
    print("\n🧪 Testing critical imports...")
    
    try:
        import django
        print(f"✅ Django {django.get_version()}")
    except ImportError:
        print("❌ Django import failed")
        
    try:
        import rest_framework
        print(f"✅ Django REST Framework {rest_framework.VERSION}")
    except ImportError:
        print("❌ Django REST Framework import failed")
        
    try:
        import channels
        print("✅ Django Channels")
    except ImportError:
        print("❌ Django Channels import failed")
    
    # Test Django setup
    print("\n🔧 Testing Django setup...")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
        import django
        django.setup()
        print("✅ Django setup successful")
        
        from django.core.management import call_command
        call_command('check', verbosity=0)
        print("✅ Django system check passed")
        
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False
    
    print("\n🎉 PACKAGE INSTALLATION COMPLETE!")
    print("✅ Express Deals is ready for development")
    print("\n💡 Next steps:")
    print("1. Run: python manage.py runserver")
    print("2. Open: http://127.0.0.1:8000/")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Installation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
