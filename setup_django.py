#!/usr/bin/env python
"""
Django management script to handle migrations and setup without terminal output dependency.
"""
import os
import sys
import django
from pathlib import Path

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    django.setup()
    
    from django.core.management import execute_from_command_line
    from django.db import connection
    from django.contrib.auth.models import User
    
    def check_database():
        """Check if database is accessible and show table info."""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                print(f"✅ Database accessible. Found {len(tables)} tables:")
                for table in tables[:10]:  # Show first 10 tables
                    print(f"  - {table[0]}")
                if len(tables) > 10:
                    print(f"  ... and {len(tables) - 10} more")
                return True
        except Exception as e:
            print(f"❌ Database error: {e}")
            return False
    
    def make_migrations():
        """Create migrations for all apps."""
        try:
            print("🔄 Creating migrations...")
            execute_from_command_line(['manage.py', 'makemigrations'])
            print("✅ Migrations created successfully")
            return True
        except Exception as e:
            print(f"❌ Migration creation error: {e}")
            return False
    
    def migrate():
        """Apply migrations."""
        try:
            print("🔄 Applying migrations...")
            execute_from_command_line(['manage.py', 'migrate'])
            print("✅ Migrations applied successfully")
            return True
        except Exception as e:
            print(f"❌ Migration error: {e}")
            return False
    
    def create_superuser_if_needed():
        """Create a superuser if none exists."""
        try:
            if not User.objects.filter(is_superuser=True).exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@expressdeals.com',
                    password='admin123'
                )
                print("✅ Superuser created: admin/admin123")
            else:
                print("✅ Superuser already exists")
            return True
        except Exception as e:
            print(f"❌ Superuser creation error: {e}")
            return False
    
    def run_checks():
        """Run Django system checks."""
        try:
            print("🔄 Running Django checks...")
            execute_from_command_line(['manage.py', 'check'])
            print("✅ Django checks passed")
            return True
        except Exception as e:
            print(f"❌ Django check error: {e}")
            return False
    
    def main():
        print("🚀 Express Deals Django Setup")
        print("=" * 40)
        
        # Run all setup tasks
        tasks = [
            ("Database Check", check_database),
            ("System Checks", run_checks),
            ("Make Migrations", make_migrations),
            ("Apply Migrations", migrate),
            ("Create Superuser", create_superuser_if_needed),
        ]
        
        results = {}
        for task_name, task_func in tasks:
            print(f"\n📋 {task_name}")
            print("-" * 20)
            results[task_name] = task_func()
        
        print("\n🎯 Setup Summary")
        print("=" * 40)
        for task_name, success in results.items():
            status = "✅ SUCCESS" if success else "❌ FAILED"
            print(f"{task_name}: {status}")
        
        all_success = all(results.values())
        if all_success:
            print("\n🎉 All setup tasks completed successfully!")
            print("🌐 Ready to start development server")
        else:
            print("\n⚠️ Some tasks failed. Check the output above.")
        
        return all_success

    if __name__ == "__main__":
        main()

except Exception as e:
    print(f"❌ Setup error: {e}")
    import traceback
    traceback.print_exc()
