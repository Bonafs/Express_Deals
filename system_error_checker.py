#!/usr/bin/env python3
"""
Express Deals System Error Checker and Fixer
This script checks for common system errors and fixes them automatically.
"""

import os
import sys
import subprocess
import importlib
from pathlib import Path

def check_python_environment():
    """Check if we're in the correct Python environment"""
    print("🐍 Checking Python Environment...")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment detected")
        return True
    else:
        print("❌ No virtual environment detected")
        return False

def check_required_packages():
    """Check if all required packages are installed"""
    print("\n📦 Checking Required Packages...")
    
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
        'python-dotenv',
        'dj-database-url',
        'psycopg2-binary',
        'stripe',
        'pillow',
        'whitenoise'
    ]
    
    missing_packages = []
    installed_packages = []
    
    for package in required_packages:
        try:
            # Special handling for packages with different import names
            import_name = package
            if package == 'rest_framework':
                import_name = 'rest_framework'
            elif package == 'python-dotenv':
                import_name = 'dotenv'
            elif package == 'dj-database-url':
                import_name = 'dj_database_url'
            elif package == 'psycopg2-binary':
                import_name = 'psycopg2'
            elif package == 'beautifulsoup4':
                import_name = 'bs4'
            elif package == 'pillow':
                import_name = 'PIL'
            
            importlib.import_module(import_name)
            print(f"✅ {package}")
            installed_packages.append(package)
        except ImportError:
            print(f"❌ {package} - NOT INSTALLED")
            missing_packages.append(package)
    
    return missing_packages, installed_packages

def install_missing_packages(missing_packages):
    """Install missing packages"""
    if not missing_packages:
        print("✅ All packages are already installed!")
        return True
    
    print(f"\n📥 Installing {len(missing_packages)} missing packages...")
    
    try:
        # Upgrade pip first
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        
        # Install missing packages
        cmd = [sys.executable, '-m', 'pip', 'install'] + missing_packages
        subprocess.check_call(cmd)
        
        print("✅ All missing packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False

def check_django_settings():
    """Check Django settings for errors"""
    print("\n🔧 Checking Django Settings...")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
        import django
        django.setup()
        
        from django.core.management import execute_from_command_line
        from django.conf import settings
        
        # Check INSTALLED_APPS
        required_apps = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'rest_framework',
            'products',
            'accounts',
            'orders',
            'payments',
            'scraping',
            'realtime'
        ]
        
        missing_apps = []
        for app in required_apps:
            if app not in settings.INSTALLED_APPS:
                missing_apps.append(app)
        
        if missing_apps:
            print(f"❌ Missing apps in INSTALLED_APPS: {missing_apps}")
            return False
        else:
            print("✅ All required apps are in INSTALLED_APPS")
        
        # Check database configuration
        if settings.DATABASES:
            print("✅ Database configuration found")
        else:
            print("❌ No database configuration found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Django settings error: {e}")
        return False

def run_django_checks():
    """Run Django system checks"""
    print("\n🔍 Running Django System Checks...")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
        
        # Run Django checks
        result = subprocess.run([
            sys.executable, 'manage.py', 'check'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Django system checks passed")
            print(result.stdout)
            return True
        else:
            print("❌ Django system checks failed")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error running Django checks: {e}")
        return False

def check_file_permissions():
    """Check for file permission issues"""
    print("\n📁 Checking File Permissions...")
    
    important_files = [
        'manage.py',
        'requirements.txt',
        'express_deals/settings.py',
        'express_deals/urls.py'
    ]
    
    permission_issues = []
    
    for file_path in important_files:
        if os.path.exists(file_path):
            if os.access(file_path, os.R_OK):
                print(f"✅ {file_path} - readable")
            else:
                print(f"❌ {file_path} - NOT readable")
                permission_issues.append(file_path)
        else:
            print(f"❌ {file_path} - NOT found")
            permission_issues.append(file_path)
    
    return len(permission_issues) == 0

def fix_common_issues():
    """Fix common Django/Python issues"""
    print("\n🔧 Fixing Common Issues...")
    
    fixes_applied = []
    
    # Fix 1: Create logs directory if it doesn't exist
    logs_dir = Path('logs')
    if not logs_dir.exists():
        logs_dir.mkdir(exist_ok=True)
        fixes_applied.append("Created logs directory")
        print("✅ Created logs directory")
    
    # Fix 2: Create media directory if it doesn't exist
    media_dir = Path('media')
    if not media_dir.exists():
        media_dir.mkdir(exist_ok=True)
        fixes_applied.append("Created media directory")
        print("✅ Created media directory")
    
    # Fix 3: Create static directory if it doesn't exist
    static_dir = Path('static')
    if not static_dir.exists():
        static_dir.mkdir(exist_ok=True)
        fixes_applied.append("Created static directory")
        print("✅ Created static directory")
    
    # Fix 4: Remove .env file if it exists (using hardcoded settings)
    env_file = Path('.env')
    if env_file.exists():
        print("⚠️  .env file found - removing (using hardcoded settings)")
        env_file.unlink()
        fixes_applied.append("Removed .env file")
        print("✅ Removed .env file - using hardcoded settings")
    else:
        print("✅ No .env file found - using hardcoded settings")
    
    return fixes_applied

def main():
    """Main system check and fix function"""
    print("🔍 EXPRESS DEALS SYSTEM ERROR CHECKER & FIXER")
    print("=" * 50)
    
    # Change to project directory
    os.chdir(Path(__file__).parent)
    
    all_checks_passed = True
    
    # 1. Check Python environment
    if not check_python_environment():
        print("⚠️  Consider activating your virtual environment")
    
    # 2. Check required packages
    missing_packages, installed_packages = check_required_packages()
    
    if missing_packages:
        print(f"\n❌ Found {len(missing_packages)} missing packages")
        install_choice = input("Do you want to install missing packages? (y/n): ")
        if install_choice.lower() == 'y':
            if not install_missing_packages(missing_packages):
                all_checks_passed = False
        else:
            all_checks_passed = False
    
    # 3. Fix common issues
    fixes_applied = fix_common_issues()
    
    # 4. Check Django settings
    if not check_django_settings():
        all_checks_passed = False
    
    # 5. Check file permissions
    if not check_file_permissions():
        all_checks_passed = False
    
    # 6. Run Django system checks
    if not run_django_checks():
        all_checks_passed = False
    
    # Summary
    print("\n" + "=" * 50)
    print("🎯 SYSTEM CHECK SUMMARY")
    print("=" * 50)
    
    if fixes_applied:
        print("🔧 Fixes Applied:")
        for fix in fixes_applied:
            print(f"   ✅ {fix}")
    
    if all_checks_passed:
        print("\n🎉 ALL SYSTEM CHECKS PASSED!")
        print("✅ Your Express Deals project is ready to run")
        print("\n💡 Next steps:")
        print("   1. Run: python manage.py migrate")
        print("   2. Run: python manage.py runserver")
        print("   3. Open: http://127.0.0.1:8000/")
    else:
        print("\n⚠️  SOME ISSUES FOUND")
        print("❌ Please review the errors above and fix them")
        print("\n💡 Common solutions:")
        print("   1. Activate virtual environment: .venv\\Scripts\\activate")
        print("   2. Install packages: pip install -r requirements.txt")
        print("   3. Check Django settings")
    
    return all_checks_passed

if __name__ == "__main__":
    main()
