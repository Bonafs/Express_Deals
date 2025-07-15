#!/usr/bin/env python
"""
Script to create test admin user on Heroku for debugging 400 error
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from django.contrib.auth.models import User

def create_test_admin():
    try:
        # Test admin credentials
        TEST_USERNAME = 'testadmin'
        TEST_EMAIL = 'testadmin@expressdeals.com'
        TEST_PASSWORD = 'TestAdmin123!'
        
        # Delete existing test admin if exists
        existing_user = User.objects.filter(username=TEST_USERNAME).first()
        if existing_user:
            existing_user.delete()
            print(f"🗑️ Deleted existing test user '{TEST_USERNAME}'")
        
        # Create new test admin user
        test_admin = User.objects.create_superuser(
            username=TEST_USERNAME,
            email=TEST_EMAIL,
            password=TEST_PASSWORD
        )
        
        print(f"🎉 Created test admin user successfully!")
        print(f"\n✅ Test Admin Login Details:")
        print(f"   Username: {TEST_USERNAME}")
        print(f"   Email: {TEST_EMAIL}")
        print(f"   Password: {TEST_PASSWORD}")
        print(f"   Staff status: {test_admin.is_staff}")
        print(f"   Superuser status: {test_admin.is_superuser}")
        
        # Show all admin users
        all_admins = User.objects.filter(is_superuser=True)
        print(f"\n📊 All Admin Users:")
        for admin in all_admins:
            print(f"   - {admin.username} ({admin.email})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating test admin: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Creating test admin user for debugging...")
    success = create_test_admin()
    if success:
        print("\n✅ Test admin user created successfully!")
        print("🔧 Use these credentials to test login:")
        print("   Username: testadmin")
        print("   Password: TestAdmin123!")
    else:
        print("\n❌ Failed to create test admin user!")
