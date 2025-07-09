#!/usr/bin/env python
"""
Express Deals - Secure Sample Users Creation
Creates sample users using credentials file or environment variables
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 
                      'express_deals.heroku_settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile


def get_sample_users():
    """Get sample user data from credentials file or environment"""
    
    # Try to get from credentials file
    try:
        import credentials
        sample_users = getattr(credentials, 'SAMPLE_USERS', [])
        if sample_users:
            print("🔐 Using sample users from credentials.py file")
            return sample_users
    except ImportError:
        print("⚠️  credentials.py file not found")
    
    # Default safe sample users (no real credentials)
    default_users = [
        {
            'username': 'demo_user_1',
            'email': 'demo1@example.com',
            'first_name': 'Demo',
            'last_name': 'User1',
            'password': 'demo_password_123',
            'profile_data': {
                'phone': '+44 20 7946 0958',
                'date_of_birth': '1990-01-15',
                'address': '123 Demo St, London, UK',
            }
        },
        {
            'username': 'demo_user_2',
            'email': 'demo2@example.com',
            'first_name': 'Demo',
            'last_name': 'User2',
            'password': 'demo_password_456',
            'profile_data': {
                'phone': '+44 20 7946 0959',
                'date_of_birth': '1985-05-22',
                'address': '456 Demo Ave, Manchester, UK',
            }
        },
        {
            'username': 'demo_user_3',
            'email': 'demo3@example.com',
            'first_name': 'Demo',
            'last_name': 'User3',
            'password': 'demo_password_789',
            'profile_data': {
                'phone': '+44 20 7946 0960',
                'date_of_birth': '1988-09-10',
                'address': '789 Demo Rd, Birmingham, UK',
            }
        }
    ]
    
    print("🔐 Using default demo users (safe for public)")
    return default_users


def create_secure_sample_users():
    """Create sample users with secure credentials management"""
    
    sample_users = get_sample_users()
    created_users = []
    
    print("👥 Creating Sample Users:")
    print("=" * 50)
    
    for user_data in sample_users:
        try:
            # Check if user already exists
            if User.objects.filter(
                username=user_data['username']
            ).exists():
                print(f"📁 User already exists: {user_data['username']}")
                continue
            
            # Create user
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            
            # Create profile if data provided
            if 'profile_data' in user_data:
                profile_data = user_data['profile_data']
                try:
                    profile = UserProfile.objects.create(
                        user=user,
                        phone=profile_data.get('phone', ''),
                        date_of_birth=profile_data.get('date_of_birth'),
                        address=profile_data.get('address', '')
                    )
                    print(f"✅ Created user with profile: {user.username}")
                except Exception as profile_error:
                    print(f"⚠️  User created but profile failed: {profile_error}")
                    print(f"✅ Created user: {user.username}")
            else:
                print(f"✅ Created user: {user.username}")
            
            created_users.append(user)
            
        except Exception as e:
            print(f"❌ Error creating user {user_data['username']}: {e}")
    
    # Summary
    print(f"\n📊 User Creation Summary:")
    print(f"   👥 Total users in database: {User.objects.count()}")
    print(f"   ✅ New users created: {len(created_users)}")
    print(f"   👑 Superusers: {User.objects.filter(is_superuser=True).count()}")
    
    return created_users


if __name__ == '__main__':
    create_secure_sample_users()
