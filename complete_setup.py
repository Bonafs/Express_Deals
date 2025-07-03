#!/usr/bin/env python
"""
Express Deals Complete Setup Script
Handles migrations, sample data, and server startup in one go.
"""
import os
import sys
import django
from pathlib import Path

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
sys.path.insert(0, str(Path(__file__).resolve().parent))

def run_setup():
    """Run complete setup process."""
    print("🚀 Express Deals Complete Setup")
    print("=" * 50)
    
    try:
        # Initialize Django
        django.setup()
        
        from django.core.management import execute_from_command_line
        from django.db import connection
        from django.contrib.auth.models import User
        
        # Step 1: Check database connection
        print("\n🔌 Step 1: Database Connection")
        print("-" * 30)
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                print("✅ Database connected successfully")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
        
        # Step 2: Run migrations
        print("\n🔄 Step 2: Database Migrations")
        print("-" * 30)
        try:
            print("Creating migrations...")
            execute_from_command_line(['manage.py', 'makemigrations'])
            print("Applying migrations...")
            execute_from_command_line(['manage.py', 'migrate'])
            print("✅ Migrations completed successfully")
        except Exception as e:
            print(f"⚠️ Migration warning: {e}")
            # Continue anyway as migrations might already exist
        
        # Step 3: Create superuser
        print("\n👤 Step 3: Admin User Creation")
        print("-" * 30)
        try:
            if not User.objects.filter(is_superuser=True).exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@expressdeals.com',
                    password='admin123',
                    first_name='Admin',
                    last_name='User'
                )
                print("✅ Superuser created: admin/admin123")
            else:
                print("✅ Superuser already exists")
        except Exception as e:
            print(f"❌ Superuser creation failed: {e}")
        
        # Step 4: Populate sample data
        print("\n🌱 Step 4: Sample Data Population")
        print("-" * 30)
        try:
            # Import and run populate script
            from populate_data import main as populate_main
            populate_main()
        except Exception as e:
            print(f"⚠️ Sample data population issue: {e}")
            # Create minimal data manually
            create_minimal_data()
        
        # Step 5: Collect static files
        print("\n📁 Step 5: Static Files Collection")
        print("-" * 30)
        try:
            execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
            print("✅ Static files collected")
        except Exception as e:
            print(f"⚠️ Static files warning: {e}")
        
        # Step 6: Final checks
        print("\n🔍 Step 6: System Checks")
        print("-" * 30)
        try:
            execute_from_command_line(['manage.py', 'check'])
            print("✅ All system checks passed")
        except Exception as e:
            print(f"⚠️ System check warnings: {e}")
        
        # Summary
        print(f"\n🎯 Setup Complete!")
        print("=" * 50)
        
        # Show stats
        from products.models import Category, Product
        print(f"📂 Categories: {Category.objects.count()}")
        print(f"🛍️ Products: {Product.objects.count()}")
        print(f"👤 Users: {User.objects.count()}")
        
        print(f"\n🌐 Ready to start development server!")
        print(f"🔑 Admin Panel: http://127.0.0.1:8000/admin/")
        print(f"🔐 Login: admin/admin123")
        print(f"\n💡 Run: python start_server.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_minimal_data():
    """Create minimal data if populate_data fails."""
    try:
        from products.models import Category, Product
        from django.utils.text import slugify
        from decimal import Decimal
        
        # Create basic category
        category, created = Category.objects.get_or_create(
            name='Electronics',
            defaults={
                'slug': 'electronics',
                'description': 'Electronic products and gadgets'
            }
        )
        
        # Create basic product
        product, created = Product.objects.get_or_create(
            name='Sample Product',
            defaults={
                'slug': 'sample-product',
                'category': category,
                'description': 'This is a sample product for testing.',
                'price': Decimal('99.99'),
                'stock_quantity': 10,
                'is_active': True,
            }
        )
        
        print("✅ Minimal data created")
        
    except Exception as e:
        print(f"⚠️ Minimal data creation failed: {e}")

if __name__ == "__main__":
    success = run_setup()
    if success:
        print("\n🎉 Express Deals is ready!")
    else:
        print("\n💔 Setup encountered issues. Check the output above.")
