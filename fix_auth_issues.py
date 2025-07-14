#!/usr/bin/env python
"""
Express Deals Authentication Issue Diagnosis and Fix
===================================================
This script diagnoses and fixes authentication issues for:
- Admin user (superuser access)
- Bonafs user (live customer access)
"""

import os
import sys
import django
from django.conf import settings

# Setup Django
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
    django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from accounts.models import UserProfile
from credentials import SUPERUSER_USERNAME, SUPERUSER_EMAIL, SUPERUSER_PASSWORD, SAMPLE_USERS

def test_authentication():
    """Test authentication for admin and bonafs users"""
    print("🔐 Testing Authentication...")
    print("=" * 50)
    
    # Test admin authentication
    print(f"Testing admin user...")
    admin_user = authenticate(username=SUPERUSER_USERNAME, password=SUPERUSER_PASSWORD)
    if admin_user:
        print(f"✅ Admin authentication SUCCESS: {admin_user.username}")
        print(f"   - Email: {admin_user.email}")
        print(f"   - Is Superuser: {admin_user.is_superuser}")
        print(f"   - Is Active: {admin_user.is_active}")
    else:
        print(f"❌ Admin authentication FAILED")
    
    print()
    
    # Test bonafs authentication
    bonafs_data = next((user for user in SAMPLE_USERS if user['username'] == 'bonafs'), None)
    if bonafs_data:
        print(f"Testing bonafs user...")
        bonafs_user = authenticate(username=bonafs_data['username'], password=bonafs_data['password'])
        if bonafs_user:
            print(f"✅ Bonafs authentication SUCCESS: {bonafs_user.username}")
            print(f"   - Email: {bonafs_user.email}")
            print(f"   - Is Superuser: {bonafs_user.is_superuser}")
            print(f"   - Is Active: {bonafs_user.is_active}")
        else:
            print(f"❌ Bonafs authentication FAILED")
    
    print()

def check_user_profiles():
    """Check user profiles for completeness"""
    print("👤 Checking User Profiles...")
    print("=" * 50)
    
    users = User.objects.all()
    for user in users:
        print(f"User: {user.username}")
        print(f"   - Email: {user.email}")
        print(f"   - Name: {user.first_name} {user.last_name}")
        print(f"   - Is Active: {user.is_active}")
        print(f"   - Is Superuser: {user.is_superuser}")
        
        try:
            profile = UserProfile.objects.get(user=user)
            print(f"   - Profile: ✅ EXISTS")
            print(f"   - Phone: {profile.phone_number or 'Not set'}")
            print(f"   - Address: {profile.address or 'Not set'}")
        except UserProfile.DoesNotExist:
            print(f"   - Profile: ❌ MISSING")
        
        print()

def fix_missing_profiles():
    """Create missing user profiles"""
    print("🔧 Fixing Missing User Profiles...")
    print("=" * 50)
    
    fixed_count = 0
    
    for user_data in SAMPLE_USERS:
        try:
            user = User.objects.get(username=user_data['username'])
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'phone_number': user_data['profile_data'].get('phone', ''),
                    'date_of_birth': user_data['profile_data'].get('date_of_birth'),
                    'address': user_data['profile_data'].get('address', ''),
                }
            )
            
            if created:
                print(f"✅ Created profile for {user.username}")
                fixed_count += 1
            else:
                print(f"ℹ️  Profile already exists for {user.username}")
                
        except User.DoesNotExist:
            print(f"❌ User {user_data['username']} not found")
    
    print(f"\n🎉 Fixed {fixed_count} user profiles")
    print()

def reset_user_passwords():
    """Reset passwords for admin and bonafs users if needed"""
    print("🔑 Resetting User Passwords...")
    print("=" * 50)
    
    # Reset admin password
    try:
        admin_user = User.objects.get(username=SUPERUSER_USERNAME)
        admin_user.set_password(SUPERUSER_PASSWORD)
        admin_user.save()
        print(f"✅ Admin password reset for {admin_user.username}")
    except User.DoesNotExist:
        print(f"❌ Admin user {SUPERUSER_USERNAME} not found")
    
    # Reset bonafs password
    bonafs_data = next((user for user in SAMPLE_USERS if user['username'] == 'bonafs'), None)
    if bonafs_data:
        try:
            bonafs_user = User.objects.get(username=bonafs_data['username'])
            bonafs_user.set_password(bonafs_data['password'])
            bonafs_user.save()
            print(f"✅ Bonafs password reset for {bonafs_user.username}")
        except User.DoesNotExist:
            print(f"❌ Bonafs user {bonafs_data['username']} not found")
    
    print()

def verify_admin_permissions():
    """Verify admin user has proper permissions"""
    print("🛡️  Verifying Admin Permissions...")
    print("=" * 50)
    
    try:
        admin_user = User.objects.get(username=SUPERUSER_USERNAME)
        
        # Ensure admin has proper permissions
        if not admin_user.is_superuser:
            admin_user.is_superuser = True
            admin_user.save()
            print("✅ Fixed: Admin is now superuser")
        
        if not admin_user.is_staff:
            admin_user.is_staff = True
            admin_user.save()
            print("✅ Fixed: Admin is now staff")
        
        if not admin_user.is_active:
            admin_user.is_active = True
            admin_user.save()
            print("✅ Fixed: Admin is now active")
        
        print(f"✅ Admin permissions verified for {admin_user.username}")
        
    except User.DoesNotExist:
        print(f"❌ Admin user {SUPERUSER_USERNAME} not found")
    
    print()

def create_admin_login_url():
    """Create admin login information"""
    print("🌐 Admin Access Information...")
    print("=" * 50)
    
    print("Admin Panel Access:")
    print(f"   URL: http://localhost:8000/admin/")
    print(f"   Username: {SUPERUSER_USERNAME}")
    print(f"   Password: {SUPERUSER_PASSWORD}")
    print()
    
    print("Customer Login Access:")
    print(f"   URL: http://localhost:8000/accounts/login/")
    bonafs_data = next((user for user in SAMPLE_USERS if user['username'] == 'bonafs'), None)
    if bonafs_data:
        print(f"   Username: {bonafs_data['username']}")
        print(f"   Password: {bonafs_data['password']}")
        print(f"   Email: {bonafs_data['email']}")
    print()

def main():
    """Main function to run all diagnostics and fixes"""
    print("🚀 Express Deals Authentication Fix")
    print("=" * 50)
    print()
    
    # Run diagnostics
    check_user_profiles()
    test_authentication()
    
    # Apply fixes
    fix_missing_profiles()
    reset_user_passwords()
    verify_admin_permissions()
    
    # Re-test after fixes
    print("🔄 Re-testing Authentication After Fixes...")
    print("=" * 50)
    test_authentication()
    
    # Provide access information
    create_admin_login_url()
    
    print("✅ Authentication fix complete!")
    print("🎯 You can now login with both admin and bonafs credentials")

if __name__ == '__main__':
    main()
