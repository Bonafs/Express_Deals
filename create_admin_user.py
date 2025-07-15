#!/usr/bin/env python
"""
Script to create/update admin user on Heroku
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from django.contrib.auth.models import User

# Admin credentials - Use environment variables for security
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'please_set_secure_password')

def create_admin_user():
    try:
        # Check if admin user exists
        admin_user = User.objects.filter(username=ADMIN_USERNAME).first()
        
        if admin_user:
            print(f"✅ Admin user '{ADMIN_USERNAME}' already exists")
            print(f"   - Email: {admin_user.email}")
            print(f"   - Is staff: {admin_user.is_staff}")
            print(f"   - Is superuser: {admin_user.is_superuser}")
            
            # Update to ensure admin has correct permissions
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.email = ADMIN_EMAIL
            admin_user.set_password(ADMIN_PASSWORD)
            admin_user.save()
            print(f"🔄 Updated admin user permissions and password")
            
        else:
            # Create new admin user
            admin_user = User.objects.create_superuser(
                username=ADMIN_USERNAME,
                email=ADMIN_EMAIL,
                password=ADMIN_PASSWORD
            )
            print(f"🎉 Created new admin user '{ADMIN_USERNAME}'")
            
        print(f"\n✅ Admin login details:")
        print(f"   Username: {ADMIN_USERNAME}")
        print(f"   Email: {ADMIN_EMAIL}")
        print(f"   Password: {ADMIN_PASSWORD}")
        print(f"   Staff status: {admin_user.is_staff}")
        print(f"   Superuser status: {admin_user.is_superuser}")
        
        # Show total users
        total_users = User.objects.count()
        superusers = User.objects.filter(is_superuser=True).count()
        print(f"\n📊 Database stats:")
        print(f"   Total users: {total_users}")
        print(f"   Superusers: {superusers}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Setting up admin user for Express Deals...")
    success = create_admin_user()
    if success:
        print("\n✅ Admin user setup complete!")
    else:
        print("\n❌ Admin user setup failed!")
