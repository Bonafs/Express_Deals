#!/usr/bin/env python
"""
Express Deals - Stripe Payment Configuration Test
Test Stripe test mode setup and demo card processing
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from django.conf import settings
import stripe

def test_stripe_configuration():
    """Test Stripe configuration and demo card processing"""
    print("💳 EXPRESS DEALS - STRIPE PAYMENT TESTING")
    print("=" * 60)
    
    # Check Stripe Configuration
    print("🔧 STRIPE CONFIGURATION:")
    print(f"   Publishable Key: {settings.STRIPE_PUBLISHABLE_KEY}")
    print(f"   Secret Key: {settings.STRIPE_SECRET_KEY}")
    print(f"   Webhook Secret: {settings.STRIPE_WEBHOOK_SECRET}")
    print()
    
    # Check if keys are test keys
    is_test_mode = (
        settings.STRIPE_PUBLISHABLE_KEY.startswith('pk_test_') and 
        settings.STRIPE_SECRET_KEY.startswith('sk_test_')
    )
    
    print(f"🧪 Test Mode: {'✅ YES' if is_test_mode else '❌ NO (LIVE MODE!)'}")
    
    # Set up Stripe API
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    # Test if credentials work (only if they're not placeholders)
    if 'development_key' not in settings.STRIPE_SECRET_KEY:
        try:
            print("\n🔍 TESTING STRIPE API CONNECTION...")
            # Try to retrieve account info
            account = stripe.Account.retrieve()
            print(f"✅ Stripe API Connected")
            print(f"   Account ID: {account.id}")
            print(f"   Country: {account.country}")
            print(f"   Charges Enabled: {account.charges_enabled}")
            
        except stripe.error.AuthenticationError:
            print("❌ Stripe API Authentication Failed - Invalid API Key")
        except stripe.error.StripeError as e:
            print(f"❌ Stripe API Error: {e}")
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
    else:
        print("⚠️ Using placeholder keys - cannot test API connection")
    
    print("\n" + "=" * 60)
    print("💳 STRIPE TEST CARDS FOR DEMO PAYMENTS")
    print("=" * 60)
    
    test_cards = [
        {
            "name": "Visa - Success",
            "number": "4242424242424242",
            "exp": "12/25",
            "cvc": "123",
            "description": "Always succeeds"
        },
        {
            "name": "Visa - Declined",
            "number": "4000000000000002",
            "exp": "12/25", 
            "cvc": "123",
            "description": "Always declined"
        },
        {
            "name": "Mastercard - Success",
            "number": "5555555555554444",
            "exp": "12/25",
            "cvc": "123", 
            "description": "Always succeeds"
        },
        {
            "name": "American Express",
            "number": "378282246310005",
            "exp": "12/25",
            "cvc": "1234",
            "description": "Always succeeds"
        },
        {
            "name": "3D Secure Required",
            "number": "4000000000003220",
            "exp": "12/25",
            "cvc": "123",
            "description": "Requires authentication"
        }
    ]
    
    for card in test_cards:
        print(f"💳 {card['name']}")
        print(f"   Number: {card['number']}")
        print(f"   Exp: {card['exp']} | CVC: {card['cvc']}")
        print(f"   Result: {card['description']}")
        print()
    
    print("=" * 60)
    print("🧪 HOW TO TEST PAYMENTS:")
    print("1. Use any test card above in your checkout form")
    print("2. Use any future expiry date (MM/YY)")
    print("3. Use any 3-digit CVC (4 digits for Amex)")
    print("4. Use any billing address")
    print("5. In test mode, no real money is charged")
    print()
    print("🔗 Payment URLs to test:")
    print("   Local: http://127.0.0.1:8000/checkout/")
    print("   Heroku: https://express-deals.herokuapp.com/checkout/")

def test_stripe_payment_intent():
    """Test creating a payment intent with demo amount"""
    if ('placeholder' in settings.STRIPE_SECRET_KEY.lower() or 
        'development_key' in settings.STRIPE_SECRET_KEY):
        print("\n⚠️ PLACEHOLDER STRIPE KEYS DETECTED")
        print("📋 TO ENABLE STRIPE PAYMENT DEMOS:")
        print("   1. Get test keys from: https://dashboard.stripe.com/test/apikeys")
        print("   2. Set environment variables:")
        print("      $env:STRIPE_PUBLISHABLE_KEY='pk_test_your_real_key'")
        print("      $env:STRIPE_SECRET_KEY='sk_test_your_real_key'")
        print("   3. Run this test again")
        print()
        print("✅ CONFIGURATION: Ready for real Stripe test keys")
        return
    
    print("\n🎯 TESTING PAYMENT INTENT CREATION...")
    
    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        # Create a test payment intent for £10.00
        intent = stripe.PaymentIntent.create(
            amount=1000,  # £10.00 in pence
            currency='gbp',
            metadata={
                'test': 'true',
                'product': 'Demo Product'
            }
        )
        
        print(f"✅ Payment Intent Created Successfully")
        print(f"   Intent ID: {intent.id}")
        print(f"   Amount: £{intent.amount / 100:.2f}")
        print(f"   Currency: {intent.currency.upper()}")
        print(f"   Status: {intent.status}")
        print(f"   Client Secret: {intent.client_secret[:20]}...")
        
    except stripe.error.StripeError as e:
        print(f"❌ Payment Intent Failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    test_stripe_configuration()
    test_stripe_payment_intent()
