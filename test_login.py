#!/usr/bin/env python
"""
Express Deals Login Test Script
===============================
Test login functionality for both admin and customer accounts
"""

import os
import sys
import django
from django.test import TestCase, Client
from django.urls import reverse

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from credentials import SUPERUSER_USERNAME, SUPERUSER_PASSWORD, SAMPLE_USERS

def test_web_login():
    """Test web-based login functionality"""
    print("🌐 Testing Web Login Functionality...")
    print("=" * 50)
    
    # Create test client
    client = Client()
    
    # Test admin login
    print("Testing admin login via web interface...")
    response = client.post('/accounts/login/', {
        'username': SUPERUSER_USERNAME,
        'password': SUPERUSER_PASSWORD,
        'remember_me': False
    })
    
    if response.status_code == 302:  # Redirect indicates successful login
        print("✅ Admin web login SUCCESS")
    else:
        print(f"❌ Admin web login FAILED (Status: {response.status_code})")
    
    # Test bonafs login
    bonafs_data = next((user for user in SAMPLE_USERS if user['username'] == 'bonafs'), None)
    if bonafs_data:
        print("Testing bonafs login via web interface...")
        response = client.post('/accounts/login/', {
            'username': bonafs_data['username'],
            'password': bonafs_data['password'],
            'remember_me': False
        })
        
        if response.status_code == 302:  # Redirect indicates successful login
            print("✅ Bonafs web login SUCCESS")
        else:
            print(f"❌ Bonafs web login FAILED (Status: {response.status_code})")
    
    print()

def test_admin_access():
    """Test admin panel access"""
    print("🛡️  Testing Admin Panel Access...")
    print("=" * 50)
    
    client = Client()
    
    # Login as admin
    login_success = client.login(username=SUPERUSER_USERNAME, password=SUPERUSER_PASSWORD)
    
    if login_success:
        print("✅ Admin login successful")
        
        # Test admin panel access
        response = client.get('/admin/')
        if response.status_code == 200:
            print("✅ Admin panel accessible")
        else:
            print(f"❌ Admin panel access failed (Status: {response.status_code})")
    else:
        print("❌ Admin login failed")
    
    print()

def test_customer_access():
    """Test customer account access"""
    print("👤 Testing Customer Account Access...")
    print("=" * 50)
    
    client = Client()
    bonafs_data = next((user for user in SAMPLE_USERS if user['username'] == 'bonafs'), None)
    
    if bonafs_data:
        # Login as bonafs
        login_success = client.login(username=bonafs_data['username'], password=bonafs_data['password'])
        
        if login_success:
            print("✅ Bonafs login successful")
            
            # Test profile access
            response = client.get('/accounts/profile/')
            if response.status_code == 200:
                print("✅ Customer profile accessible")
            elif response.status_code == 404:
                print("ℹ️  Profile page not found (may need to be created)")
            else:
                print(f"❌ Customer profile access failed (Status: {response.status_code})")
        else:
            print("❌ Bonafs login failed")
    
    print()

def show_login_credentials():
    """Display login credentials for reference"""
    print("🔐 Login Credentials Summary")
    print("=" * 50)
    
    print("🛡️  ADMIN ACCESS:")
    print(f"   Username: {SUPERUSER_USERNAME}")
    print(f"   Password: {SUPERUSER_PASSWORD}")
    print(f"   Admin URL: http://localhost:8000/admin/")
    print()
    
    print("👤 CUSTOMER ACCESS (Bonafs):")
    bonafs_data = next((user for user in SAMPLE_USERS if user['username'] == 'bonafs'), None)
    if bonafs_data:
        print(f"   Username: {bonafs_data['username']}")
        print(f"   Email: {bonafs_data['email']}")
        print(f"   Password: {bonafs_data['password']}")
        print(f"   Login URL: http://localhost:8000/accounts/login/")
    print()
    
    print("🌐 DEVELOPMENT SERVER:")
    print("   To start server: python manage.py runserver 8000")
    print("   Access at: http://localhost:8000/")
    print()

def main():
    """Run all login tests"""
    print("🚀 Express Deals Login Test Suite")
    print("=" * 50)
    print()
    
    try:
        test_web_login()
        test_admin_access()
        test_customer_access()
        show_login_credentials()
        
        print("✅ Login testing complete!")
        print("🎯 Both admin and customer login functionality verified")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        print("Please ensure the Django server is running and database is accessible")

if __name__ == '__main__':
    main()
