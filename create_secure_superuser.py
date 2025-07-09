#!/usr/bin/env python
"""
Express Deals - Secure Superuser Creation
Creates superuser using environment variables or secure credentials file
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 
                      'express_deals.settings')
django.setup()

from django.contrib.auth.models import User


def get_credentials():
    """Get superuser credentials from environment or credentials file"""
    
    # Try environment variables first (production)
    username = os.environ.get('SUPERUSER_USERNAME')
    email = os.environ.get('SUPERUSER_EMAIL')
    password = os.environ.get('SUPERUSER_PASSWORD')
    
    if username and email and password:
        print("🔐 Using credentials from environment variables")
        return username, email, password
    
    # Try credentials file (development)
    try:
        import credentials
        username = getattr(credentials, 'SUPERUSER_USERNAME', None)
        email = getattr(credentials, 'SUPERUSER_EMAIL', None)
        password = getattr(credentials, 'SUPERUSER_PASSWORD', None)
        
        if username and email and password:
            print("🔐 Using credentials from credentials.py file")
            return username, email, password
    except ImportError:
        print("⚠️  credentials.py file not found")
    
    # Fallback to prompting user
    print("🔑 No credentials found in environment or file")
    print("Please enter superuser credentials:")
    username = input("Username: ").strip()
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    
    if not all([username, email, password]):
        print("❌ All fields are required!")
        sys.exit(1)
    
    return username, email, password


def create_secure_superuser():
    """Create superuser with secure credentials"""
    try:
        username, email, password = get_credentials()
        
        if User.objects.filter(username=username).exists():
            print(f'ℹ️  Superuser "{username}" already exists!')
            return
        
        # Create superuser
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        print(f'✅ Superuser "{username}" created successfully!')
        print(f'📧 Email: {email}')
        print('🌐 Access admin at: https://express-deals.herokuapp.com/admin/')
        
        # Verify creation
        total_users = User.objects.count()
        superusers = User.objects.filter(is_superuser=True).count()
        print(f'📊 Total users: {total_users} (Superusers: {superusers})')
        
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")
        sys.exit(1)


if __name__ == '__main__':
    create_secure_superuser()
