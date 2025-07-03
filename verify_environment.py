#!/usr/bin/env python
"""
Express Deals Environment Verification Script
This script checks if all required packages are installed in the correct environment
"""

import sys
import subprocess
import os

def check_environment():
    """Check the current Python environment and package installations"""
    
    print("🚀 Express Deals - Environment Verification")
    print("=" * 50)
    
    # Check Python version and executable path
    print(f"🐍 Python Version: {sys.version}")
    print(f"📍 Python Executable: {sys.executable}")
    print(f"📂 Current Working Directory: {os.getcwd()}")
    
    # List of required packages for Express Deals
    required_packages = [
        'django',
        'rest_framework',
        'celery',
        'channels',
        'scrapy',
        'beautifulsoup4',
        'requests',
        'redis',
        'twilio',
        'sentry_sdk',
        'pandas',
        'numpy'
    ]
    
    print("\n🔍 Checking Required Packages:")
    print("-" * 30)
    
    installed_packages = []
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'rest_framework':
                import rest_framework
                version = '.'.join(map(str, rest_framework.VERSION))
                print(f"✅ {package}: {version}")
                installed_packages.append(f"{package}=={version}")
            elif package == 'django':
                import django
                print(f"✅ {package}: {django.get_version()}")
                installed_packages.append(f"{package}=={django.get_version()}")
            elif package == 'celery':
                import celery
                print(f"✅ {package}: {celery.__version__}")
                installed_packages.append(f"{package}=={celery.__version__}")
            elif package == 'channels':
                import channels
                print(f"✅ {package}: {channels.__version__}")
                installed_packages.append(f"{package}=={channels.__version__}")
            elif package == 'scrapy':
                import scrapy
                print(f"✅ {package}: {scrapy.__version__}")
                installed_packages.append(f"{package}=={scrapy.__version__}")
            else:
                module = __import__(package)
                if hasattr(module, '__version__'):
                    version = module.__version__
                    print(f"✅ {package}: {version}")
                    installed_packages.append(f"{package}=={version}")
                else:
                    print(f"✅ {package}: installed")
                    installed_packages.append(package)
                    
        except ImportError:
            print(f"❌ {package}: NOT INSTALLED")
            missing_packages.append(package)
        except Exception as e:
            print(f"⚠️  {package}: ERROR - {e}")
            missing_packages.append(package)
    
    print(f"\n📊 Summary:")
    print(f"✅ Installed: {len(installed_packages)}")
    print(f"❌ Missing: {len(missing_packages)}")
    
    if missing_packages:
        print(f"\n🔧 Missing packages that need to be installed:")
        for package in missing_packages:
            print(f"   - {package}")
        
        print(f"\n💡 To install missing packages, run:")
        print(f"   pip install {' '.join(missing_packages)}")
    else:
        print(f"\n🎉 All required packages are installed!")
    
    # Test Django configuration
    print(f"\n🔧 Testing Django Configuration:")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
        import django
        django.setup()
        
        from django.conf import settings
        
        if 'rest_framework' in settings.INSTALLED_APPS:
            print("✅ Django REST Framework configured in settings")
        else:
            print("❌ Django REST Framework NOT in INSTALLED_APPS")
            
        if 'scraping' in settings.INSTALLED_APPS:
            print("✅ Scraping app configured in settings")
        else:
            print("⚠️  Scraping app NOT in INSTALLED_APPS")
            
        if 'realtime' in settings.INSTALLED_APPS:
            print("✅ Realtime app configured in settings")
        else:
            print("⚠️  Realtime app NOT in INSTALLED_APPS")
            
        print("✅ Django configuration is valid")
        
    except Exception as e:
        print(f"❌ Django configuration error: {e}")
    
    return len(missing_packages) == 0

if __name__ == "__main__":
    success = check_environment()
    
    if success:
        print(f"\n🚀 Express Deals environment is ready for production!")
        sys.exit(0)
    else:
        print(f"\n⚠️  Please install missing packages before proceeding.")
        sys.exit(1)
