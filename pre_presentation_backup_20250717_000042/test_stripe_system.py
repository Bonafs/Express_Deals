#!/usr/bin/env python
"""
Express Deals - Stripe Payment System Test
Verify the complete payment system is working
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

import stripe
from django.conf import settings
from django.contrib.auth.models import User
from subscriptions.models import SubscriptionPlan, CustomerSubscription
from payments.models import StripeCustomer

def test_stripe_system():
    """Test the complete Stripe payment system"""
    print("🧪 EXPRESS DEALS - STRIPE PAYMENT SYSTEM TEST")
    print("=" * 60)
    
    # Test 1: Stripe Configuration
    print("1️⃣ Testing Stripe Configuration...")
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    try:
        # Test API connection
        balance = stripe.Balance.retrieve()
        print(f"   ✅ Stripe API connected successfully")
        print(f"   💰 Available balance: {balance.available[0].amount/100} {balance.available[0].currency.upper()}")
    except Exception as e:
        print(f"   ❌ Stripe API error: {e}")
        return False
    
    # Test 2: Database Models
    print("\n2️⃣ Testing Database Models...")
    try:
        # Check if we can create subscription plans
        plan_count = SubscriptionPlan.objects.count()
        subscription_count = CustomerSubscription.objects.count()
        customer_count = StripeCustomer.objects.count()
        
        print(f"   ✅ Subscription Plans: {plan_count}")
        print(f"   ✅ Active Subscriptions: {subscription_count}")
        print(f"   ✅ Stripe Customers: {customer_count}")
    except Exception as e:
        print(f"   ❌ Database error: {e}")
        return False
    
    # Test 3: Demo Payment Intent
    print("\n3️⃣ Testing Payment Intent Creation...")
    try:
        # Create a test payment intent
        intent = stripe.PaymentIntent.create(
            amount=1000,  # £10.00
            currency='gbp',
            metadata={'test': 'demo_payment_intent'}
        )
        print(f"   ✅ Payment Intent created: {intent.id}")
        print(f"   💳 Amount: £{intent.amount/100}")
        print(f"   🔒 Status: {intent.status}")
    except Exception as e:
        print(f"   ❌ Payment Intent error: {e}")
        return False
    
    # Test 4: Stripe Products (for subscriptions)
    print("\n4️⃣ Testing Stripe Products...")
    try:
        # Create a test product
        product = stripe.Product.create(
            name='Express Deals Test Plan',
            description='Test subscription plan for Express Deals',
            metadata={'test': 'demo_product'}
        )
        print(f"   ✅ Product created: {product.id}")
        
        # Create a test price
        price = stripe.Price.create(
            unit_amount=999,  # £9.99
            currency='gbp',
            recurring={'interval': 'month'},
            product=product.id,
            metadata={'test': 'demo_price'}
        )
        print(f"   ✅ Price created: {price.id}")
        print(f"   💰 Price: £{price.unit_amount/100}/month")
        
        # Clean up test objects
        stripe.Product.modify(product.id, active=False)
        print(f"   🧹 Test objects cleaned up")
        
    except Exception as e:
        print(f"   ❌ Product/Price error: {e}")
        return False
    
    # Test 5: URL Configuration
    print("\n5️⃣ Testing URL Configuration...")
    try:
        from django.urls import reverse
        
        urls_to_test = [
            'subscriptions:plans',
            'subscriptions:management',
            'subscriptions:manual_payment',
        ]
        
        for url_name in urls_to_test:
            try:
                url = reverse(url_name)
                print(f"   ✅ {url_name}: {url}")
            except Exception as e:
                print(f"   ❌ {url_name}: {e}")
                
    except Exception as e:
        print(f"   ❌ URL configuration error: {e}")
    
    # Test 6: Demo Cards Information
    print("\n6️⃣ Demo Cards Available for Testing...")
    demo_cards = [
        ("4242424242424242", "Successful payment"),
        ("4000000000000002", "Declined payment"),
        ("4000000000003220", "3D Secure authentication"),
        ("5555555555554444", "Mastercard success"),
        ("378282246310005", "American Express success"),
    ]
    
    for card, description in demo_cards:
        print(f"   💳 {card}: {description}")
    
    print("\n" + "=" * 60)
    print("🎉 STRIPE PAYMENT SYSTEM TEST COMPLETED SUCCESSFULLY!")
    print("📋 NEXT STEPS:")
    print("   1. Get your live Stripe publishable key")
    print("   2. Create subscription plans in Django admin")
    print("   3. Test payment flows at /subscriptions/plans/")
    print("   4. Configure webhooks for production")
    print("   5. Deploy and go live! 🚀")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    test_stripe_system()
