#!/usr/bin/env python
"""
Sample users creation script for Express Deals
Run this to populate your database with sample users
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.heroku_settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Profile

def create_sample_users():
    """Create sample users with profiles"""
    
    sample_users = [
        {
            'username': 'john_doe',
            'email': 'john.doe@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'express_deals_123',
            'profile_data': {
                'phone': '+1234567890',
                'date_of_birth': '1990-01-15',
                'address': '123 Main St, New York, NY 10001',
            }
        },
        {
            'username': 'jane_smith',
            'email': 'jane.smith@example.com',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'password': 'express_deals_456',
            'profile_data': {
                'phone': '+1234567891',
                'date_of_birth': '1985-05-22',
                'address': '456 Oak Ave, Los Angeles, CA 90210',
            }
        },
        {
            'username': 'mike_johnson',
            'email': 'mike.johnson@example.com',
            'first_name': 'Mike',
            'last_name': 'Johnson',
            'password': 'express_deals_789',
            'profile_data': {
                'phone': '+1234567892',
                'date_of_birth': '1992-08-10',
                'address': '789 Pine Rd, Chicago, IL 60601',
            }
        },
        {
            'username': 'sarah_wilson',
            'email': 'sarah.wilson@example.com',
            'first_name': 'Sarah',
            'last_name': 'Wilson',
            'password': 'express_deals_012',
            'profile_data': {
                'phone': '+1234567893',
                'date_of_birth': '1988-12-03',
                'address': '012 Elm St, Miami, FL 33101',
            }
        },
        {
            'username': 'demo_user',
            'email': 'demo@expressdeals.com',
            'first_name': 'Demo',
            'last_name': 'User',
            'password': 'demo123',
            'profile_data': {
                'phone': '+1234567894',
                'date_of_birth': '1995-03-20',
                'address': '999 Demo Ave, Seattle, WA 98101',
            }
        },
    ]
    
    created_users = []
    for user_data in sample_users:
        try:
            # Create user
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                }
            )
            
            if created:
                user.set_password(user_data['password'])
                user.save()
                print(f"✅ Created user: {user.username} ({user.email})")
                
                # Try to create profile if Profile model exists
                try:
                    profile_data = user_data['profile_data']
                    profile, profile_created = Profile.objects.get_or_create(
                        user=user,
                        defaults={
                            'phone': profile_data.get('phone', ''),
                            'date_of_birth': profile_data.get('date_of_birth'),
                            'address': profile_data.get('address', ''),
                        }
                    )
                    if profile_created:
                        print(f"   📝 Created profile for {user.username}")
                except Exception as e:
                    print(f"   ⚠️ Could not create profile for {user.username}: {e}")
                    
            else:
                print(f"👤 User already exists: {user.username}")
                
            created_users.append(user)
            
        except Exception as e:
            print(f"❌ Error creating user {user_data['username']}: {e}")
    
    print(f"\n🎉 Sample users creation complete!")
    print(f"👥 Total users: {User.objects.count()}")
    print(f"🔐 Superusers: {User.objects.filter(is_superuser=True).count()}")
    print(f"👤 Regular users: {User.objects.filter(is_superuser=False).count()}")
    
    print(f"\n📋 User Login Credentials:")
    print(f"=" * 50)
    for user_data in sample_users:
        print(f"Username: {user_data['username']}")
        print(f"Email: {user_data['email']}")
        print(f"Password: {user_data['password']}")
        print(f"-" * 25)

if __name__ == '__main__':
    create_sample_users()
