#!/usr/bin/env python
"""
Express Deals Production Deployment Script
Automates the deployment process and runs necessary checks.
"""
import os
import sys
import subprocess
import django
from pathlib import Path

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
sys.path.insert(0, str(Path(__file__).resolve().parent))

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout:
                print(f"Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} failed")
            if result.stderr:
                print(f"Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False

def check_environment():
    """Check if all required environment variables are set."""
    print("\n🔍 Checking Environment Variables")
    print("-" * 40)
    
    required_vars = [
        'SECRET_KEY',
        'STRIPE_PUBLISHABLE_KEY',
        'STRIPE_SECRET_KEY',
    ]
    
    optional_vars = [
        'DATABASE_URL',
        'ALLOWED_HOSTS',
        'EMAIL_HOST',
        'AWS_ACCESS_KEY_ID',
    ]
    
    missing_required = []
    
    for var in required_vars:
        if os.getenv(var):
            print(f"✅ {var}: Set")
        else:
            print(f"❌ {var}: Missing")
            missing_required.append(var)
    
    print(f"\nOptional environment variables:")
    for var in optional_vars:
        if os.getenv(var):
            print(f"✅ {var}: Set")
        else:
            print(f"⚠️ {var}: Not set (optional)")
    
    return len(missing_required) == 0, missing_required

def collect_static_files():
    """Collect static files for production."""
    return run_command(
        "python manage.py collectstatic --noinput",
        "Collecting static files"
    )

def run_migrations():
    """Run database migrations."""
    return run_command(
        "python manage.py migrate",
        "Running database migrations"
    )

def create_superuser():
    """Create superuser if it doesn't exist."""
    print("\n👤 Creating superuser")
    print("-" * 30)
    
    try:
        django.setup()
        from django.contrib.auth.models import User
        
        if not User.objects.filter(is_superuser=True).exists():
            print("No superuser found. Creating one...")
            username = input("Enter superuser username: ").strip()
            email = input("Enter superuser email: ").strip()
            
            if username and email:
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password='admin123'  # Default password - should be changed
                )
                print(f"✅ Superuser '{username}' created successfully")
                print("⚠️ Default password is 'admin123' - Please change it immediately!")
                return True
            else:
                print("❌ Username and email are required")
                return False
        else:
            print("✅ Superuser already exists")
            return True
            
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")
        return False

def populate_sample_data():
    """Populate sample data if database is empty."""
    print("\n📦 Checking sample data")
    print("-" * 30)
    
    try:
        django.setup()
        from products.models import Category, Product
        
        if Category.objects.count() == 0:
            print("No categories found. Populating sample data...")
            return run_command(
                "python populate_data.py",
                "Populating sample data"
            )
        else:
            print(f"✅ Found {Category.objects.count()} categories")
            print(f"✅ Found {Product.objects.count()} products")
            return True
            
    except Exception as e:
        print(f"❌ Error checking sample data: {e}")
        return False

def run_tests():
    """Run the test suite."""
    return run_command(
        "python test_comprehensive.py",
        "Running comprehensive tests"
    )

def check_security():
    """Run Django security checks."""
    return run_command(
        "python manage.py check --deploy",
        "Running security checks"
    )

def main():
    """Main deployment process."""
    print("🚀 Express Deals Production Deployment")
    print("=" * 50)
    
    steps = [
        ("Environment Check", check_environment),
        ("Database Migrations", run_migrations),
        ("Static Files Collection", collect_static_files),
        ("Sample Data Population", populate_sample_data),
        ("Superuser Creation", create_superuser),
        ("Comprehensive Tests", run_tests),
        ("Security Checks", check_security),
    ]
    
    results = {}
    failed_steps = []
    
    for step_name, step_func in steps:
        try:
            if step_name == "Environment Check":
                success, missing = step_func()
                results[step_name] = success
                if not success:
                    failed_steps.append(f"{step_name}: Missing {', '.join(missing)}")
            else:
                results[step_name] = step_func()
                if not results[step_name]:
                    failed_steps.append(step_name)
        except Exception as e:
            print(f"❌ {step_name} failed with exception: {e}")
            results[step_name] = False
            failed_steps.append(f"{step_name}: {str(e)}")
    
    # Summary
    print(f"\n📊 Deployment Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for step_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{step_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n🎯 Overall Result: {passed}/{total} steps completed")
    
    if passed == total:
        print("\n🎉 DEPLOYMENT READY!")
        print("Your Express Deals platform is ready for production deployment.")
        print("\nNext steps:")
        print("1. Set up your production server (Heroku, Railway, DigitalOcean, etc.)")
        print("2. Configure your domain and SSL certificate")
        print("3. Set up monitoring and backups")
        print("4. Test the live site thoroughly")
        print("5. Set up Stripe webhooks for your production domain")
    elif passed >= total - 1:
        print("\n⚠️ MOSTLY READY")
        print("Your platform is mostly ready but has some minor issues:")
        for step in failed_steps:
            print(f"  - {step}")
        print("\nYou can proceed with deployment but should address these issues.")
    else:
        print("\n❌ NOT READY FOR DEPLOYMENT")
        print("Several critical issues need to be resolved:")
        for step in failed_steps:
            print(f"  - {step}")
        print("\nPlease fix these issues before deploying to production.")
    
    return passed >= total - 1

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
