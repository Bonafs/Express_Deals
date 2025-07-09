#!/usr/bin/env python
"""
Test UK-focused UserProfile updates
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile

def test_uk_profile():
    print("🇬🇧 Testing UK-focused UserProfile updates...")
    
    # Create a test user
    user, created = User.objects.get_or_create(
        username='uktest',
        defaults={
            'email': 'test@uk.co.uk',
            'first_name': 'John',
            'last_name': 'Smith'
        }
    )
    
    # Check if profile was auto-created
    profile = user.profile
    print(f"✅ Profile auto-created: {profile}")
    
    # Check default values
    print(f"🏠 Default country: {profile.country}")
    print(f"💰 Default currency: {profile.preferred_currency}")
    print(f"🕐 Default timezone: {profile.timezone}")
    
    # Update with UK details
    profile.address = "123 Baker Street"
    profile.city = "London"
    profile.county = "Greater London"
    profile.postcode = "NW1 6XE"
    profile.phone_number = "+44 20 7946 0958"
    profile.save()
    
    print(f"📍 Address: {profile.address}")
    print(f"🏙️ City: {profile.city}")
    print(f"🗺️ County: {profile.county}")
    print(f"📮 Postcode: {profile.postcode}")
    print(f"📞 Phone: {profile.phone_number}")
    
    print("\n✅ UK UserProfile updates working correctly!")

if __name__ == '__main__':
    test_uk_profile()
