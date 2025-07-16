#!/usr/bin/env python
"""
Express Deals - Stripe Demo Card Payment Test
Test actual payment processing with Stripe test cards
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from django.conf import settings
import stripe

def test_demo_payment():
    """Test actual payment processing with demo cards"""
    print("💳 EXPRESS DEALS - STRIPE DEMO PAYMENT TEST")
    print("=" * 60)
    
    # Set up Stripe
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    print(f"🔧 Using Stripe Key: {settings.STRIPE_SECRET_KEY[:20]}...")
    print(f"🧪 Test Mode: {'YES' if 'test' in settings.STRIPE_SECRET_KEY else 'NO'}")
    print()
    
    # Demo test cards with expected results
    test_scenarios = [
        {
            "name": "✅ Successful Payment",
            "card": "4242424242424242",
            "expected": "success"
        },
        {
            "name": "❌ Declined Payment", 
            "card": "4000000000000002",
            "expected": "declined"
        },
        {
            "name": "🔐 Requires Authentication",
            "card": "4000000000003220", 
            "expected": "requires_action"
        }
    ]
    
    for scenario in test_scenarios:
        print(f"🧪 Testing: {scenario['name']}")
        print(f"   Card: {scenario['card']}")
        
        try:
            # Create payment method
            payment_method = stripe.PaymentMethod.create(
                type="card",
                card={
                    "number": scenario['card'],
                    "exp_month": 12,
                    "exp_year": 2025,
                    "cvc": "123",
                },
            )
            
            # Create payment intent
            intent = stripe.PaymentIntent.create(
                amount=1000,  # £10.00
                currency='gbp',
                payment_method=payment_method.id,
                confirm=True,
                return_url='https://express-deals.herokuapp.com/payment/success/',
                metadata={
                    'test_scenario': scenario['name'],
                    'demo': 'true'
                }
            )
            
            print(f"   ✅ Result: {intent.status}")
            print(f"   Intent ID: {intent.id}")
            
            if intent.status == 'requires_action':
                print(f"   🔐 Next Action: {intent.next_action.type}")
            elif intent.status == 'succeeded':
                print(f"   💰 Amount: £{intent.amount/100:.2f}")
                
        except stripe.error.CardError as e:
            print(f"   ❌ Card Error: {e.user_message}")
        except stripe.error.StripeError as e:
            print(f"   ❌ Stripe Error: {e}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()

def print_demo_instructions():
    """Print comprehensive demo instructions"""
    print("=" * 60)
    print("🎯 EXPRESS DEALS - PAYMENT DEMO INSTRUCTIONS")
    print("=" * 60)
    
    print("💳 STRIPE TEST CARDS FOR LIVE DEMOS:")
    print()
    
    demo_cards = [
        {
            "purpose": "✅ Successful Payment Demo",
            "card": "4242 4242 4242 4242",
            "exp": "12/25",
            "cvc": "123",
            "result": "Payment succeeds immediately"
        },
        {
            "purpose": "❌ Declined Payment Demo", 
            "card": "4000 0000 0000 0002",
            "exp": "12/25",
            "cvc": "123",
            "result": "Payment is declined"
        },
        {
            "purpose": "🔐 3D Secure Authentication Demo",
            "card": "4000 0000 0000 3220",
            "exp": "12/25", 
            "cvc": "123",
            "result": "Requires customer authentication"
        },
        {
            "purpose": "💳 Mastercard Success Demo",
            "card": "5555 5555 5555 4444",
            "exp": "12/25",
            "cvc": "123", 
            "result": "Payment succeeds immediately"
        },
        {
            "purpose": "💎 American Express Demo",
            "card": "3782 822463 10005",
            "exp": "12/25",
            "cvc": "1234",
            "result": "Payment succeeds immediately"
        }
    ]
    
    for card in demo_cards:
        print(f"🎯 {card['purpose']}")
        print(f"   Card Number: {card['card']}")
        print(f"   Expiry: {card['exp']} | CVC: {card['cvc']}")
        print(f"   Expected: {card['result']}")
        print()
    
    print("=" * 60)
    print("🌐 DEMO URLS:")
    print(f"   🏠 Local: http://127.0.0.1:8000/")
    print(f"   ☁️ Heroku: https://express-deals.herokuapp.com/")
    print(f"   🛒 Checkout: https://express-deals.herokuapp.com/checkout/")
    print()
    
    print("📋 DEMO STEPS:")
    print("1. Visit the Express Deals website")
    print("2. Browse products and add items to cart")
    print("3. Go to checkout")
    print("4. Fill in shipping information")
    print("5. Use any test card above for payment")
    print("6. Use any future expiry date")
    print("7. Use any billing address")
    print("8. Complete the demo payment")
    print()
    
    print("⚠️ IMPORTANT DEMO NOTES:")
    print("• All payments are in TEST MODE - no real money charged")
    print("• Test cards work instantly without real card verification")
    print("• You can test successful and failed payments")
    print("• Perfect for demonstrating payment flows to customers")
    print("• All demo transactions appear in Stripe test dashboard")

if __name__ == "__main__":
    if 'development_key' not in settings.STRIPE_SECRET_KEY:
        test_demo_payment()
    print_demo_instructions()
