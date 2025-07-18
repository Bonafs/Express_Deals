#!/usr/bin/env python
"""
EXPRESS DEALS - DATABASE RESET
Reset the database to fix schema issues
"""

import os
import django
import sqlite3

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from django.db import connection
from django.core.management import call_command

def reset_database():
    """Reset the database completely"""
    print("🔄 RESETTING DATABASE...")
    
    # Get database path
    db_path = connection.settings_dict['NAME']
    print(f"📁 Database path: {db_path}")
    
    # Check if database exists
    if os.path.exists(db_path):
        print("📋 Database exists, checking tables...")
        
        # Check existing tables
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"📊 Found {len(tables)} tables: {[t[0] for t in tables]}")
            
            # Drop scraping tables if they exist
            scraping_tables = [t[0] for t in tables if 'scraping' in t[0]]
            if scraping_tables:
                print(f"🗑️ Dropping scraping tables: {scraping_tables}")
                for table in scraping_tables:
                    try:
                        cursor.execute(f"DROP TABLE IF EXISTS {table};")
                        print(f"✅ Dropped {table}")
                    except Exception as e:
                        print(f"⚠️ Error dropping {table}: {e}")
    
    # Run fresh migrations
    print("\n🔄 Running fresh migrations...")
    try:
        call_command('makemigrations', 'scraping', verbosity=2)
        print("✅ Created fresh migrations")
        
        call_command('migrate', verbosity=2)
        print("✅ Applied all migrations")
        
        # Test the models
        print("\n🧪 Testing models...")
        from scraping.models import ScrapeTarget
        
        # Create a test target
        test_target = ScrapeTarget.objects.create(
            name="Test Target",
            base_url="https://example.com",
            target_type="category",
            is_active=True
        )
        print(f"✅ Created test target: {test_target}")
        
        # Delete the test target
        test_target.delete()
        print("✅ Deleted test target")
        
        print("\n🎉 DATABASE RESET SUCCESSFUL!")
        return True
        
    except Exception as e:
        print(f"❌ Migration error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = reset_database()
    exit(0 if success else 1)
