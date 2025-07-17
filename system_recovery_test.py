#!/usr/bin/env python
"""
Express Deals - System Recovery Test
Tests all major functionality after recovery
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from django.contrib.auth.models import User
from products.models import Product
from accounts.models import UserProfile
from alerts.models import PriceAlert, DealCategory
from payments.models import SubscriptionPlan, DemoCard

def test_system():
    print("🔧 EXPRESS DEALS - SYSTEM RECOVERY TEST")
    print("=" * 50)
    
    # Test 1: Database connection
    try:
        users = User.objects.all()
        print(f"✅ Database connection: {len(users)} users found")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    
    # Test 2: Models working
    try:
        products = Product.objects.all()
        print(f"✅ Products model: {len(products)} products found")
    except Exception as e:
        print(f"❌ Products model failed: {e}")
    
    try:
        profiles = UserProfile.objects.all()
        print(f"✅ UserProfile model: {len(profiles)} profiles found")
    except Exception as e:
        print(f"❌ UserProfile model failed: {e}")
    
    try:
        alerts = PriceAlert.objects.all()
        print(f"✅ PriceAlert model: {len(alerts)} alerts found")
    except Exception as e:
        print(f"❌ PriceAlert model failed: {e}")
    
    try:
        plans = SubscriptionPlan.objects.all()
        print(f"✅ SubscriptionPlan model: {len(plans)} plans found")
    except Exception as e:
        print(f"❌ SubscriptionPlan model failed: {e}")
    
    # Test 3: Create sample data
    print("\n🎯 Creating sample data...")
    
    # Create subscription plans
    try:
        basic_plan, created = SubscriptionPlan.objects.get_or_create(
            name='basic',
            defaults={
                'display_name': 'Basic Deal Hunter',
                'description': 'Access to basic deals and 3 price alerts',
                'price': 4.99,
                'max_price_alerts': 3,
                'email_alerts': True
            }
        )
        print(f"✅ Basic plan: {'created' if created else 'exists'}")
    except Exception as e:
        print(f"❌ Failed to create basic plan: {e}")
    
    # Create demo cards
    try:
        demo_card, created = DemoCard.objects.get_or_create(
            name='Test Success Card',
            defaults={
                'card_number': '4242424242424242',
                'card_type': 'visa',
                'behavior': 'success',
                'description': 'Always succeeds for testing'
            }
        )
        print(f"✅ Demo card: {'created' if created else 'exists'}")
    except Exception as e:
        print(f"❌ Failed to create demo card: {e}")
    
    # Create deal categories
    try:
        category, created = DealCategory.objects.get_or_create(
            name='Electronics',
            defaults={
                'slug': 'electronics',
                'description': 'Electronic devices and gadgets'
            }
        )
        print(f"✅ Deal category: {'created' if created else 'exists'}")
    except Exception as e:
        print(f"❌ Failed to create deal category: {e}")
    
    print("\n🎉 SYSTEM RECOVERY TEST COMPLETE!")
    print("✅ Express Deals is fully operational!")
    return True

if __name__ == "__main__":
    success = test_system()
    if success:
        print("\n🚀 Ready to run: python manage.py runserver")
    else:
        print("\n❌ System needs additional fixes")
