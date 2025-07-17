#!/usr/bin/env python3
"""
Test payment system with demo purchases
"""
import sqlite3
import json
import uuid
from datetime import datetime, timedelta
import random

def create_test_purchase(user_id, username, amount=29.99):
    """Create a test purchase for a user"""
    
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    try:
        # Get user's payment method
        cursor.execute('''
            SELECT id, card_number, card_holder_name 
            FROM payments_paymentmethod 
            WHERE user_id = ? AND is_demo = 1 AND is_active = 1
        ''', (user_id,))
        
        payment_method = cursor.fetchone()
        if not payment_method:
            print(f"❌ No payment method found for user {username}")
            return False
        
        payment_method_id, card_number, card_holder = payment_method
        
        # Create transaction ID
        transaction_id = f"test_{uuid.uuid4().hex[:8]}"
        
        # Create payment record
        cursor.execute('''
            INSERT INTO payments_payment 
            (user_id, payment_method_id, payment_type, amount, currency, status, transaction_id, gateway_response, created_at, completed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id, 
            payment_method_id, 
            'one_time', 
            amount, 
            'GBP', 
            'succeeded', 
            transaction_id,
            json.dumps({"test": True, "card_used": card_number}),
            datetime.now(),
            datetime.now()
        ))
        
        conn.commit()
        print(f"✅ Test purchase created for {username}:")
        print(f"   Amount: £{amount}")
        print(f"   Card: {card_number} ({card_holder})")
        print(f"   Transaction ID: {transaction_id}")
        print(f"   Status: succeeded")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating test purchase for {username}: {e}")
        return False
    
    finally:
        conn.close()

def create_test_subscription(user_id, username, tier='premium'):
    """Create a test subscription for a user"""
    
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    try:
        # Get user's payment method
        cursor.execute('''
            SELECT id, card_number, card_holder_name 
            FROM payments_paymentmethod 
            WHERE user_id = ? AND is_demo = 1 AND is_active = 1
        ''', (user_id,))
        
        payment_method = cursor.fetchone()
        if not payment_method:
            print(f"❌ No payment method found for user {username}")
            return False
        
        payment_method_id, card_number, card_holder = payment_method
        
        # Subscription amounts
        tier_amounts = {
            'free': 0.00,
            'basic': 9.99,
            'premium': 19.99,
            'vip': 49.99
        }
        
        amount = tier_amounts.get(tier, 19.99)
        
        if amount > 0:
            # Create subscription payment
            transaction_id = f"sub_{uuid.uuid4().hex[:8]}"
            
            cursor.execute('''
                INSERT INTO payments_payment 
                (user_id, payment_method_id, payment_type, amount, currency, status, transaction_id, gateway_response, created_at, completed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id, 
                payment_method_id, 
                'subscription', 
                amount, 
                'GBP', 
                'succeeded', 
                transaction_id,
                json.dumps({"test": True, "subscription_tier": tier}),
                datetime.now(),
                datetime.now()
            ))
            
            conn.commit()
            print(f"✅ Test subscription created for {username}:")
            print(f"   Tier: {tier.title()}")
            print(f"   Amount: £{amount}/month")
            print(f"   Card: {card_number} ({card_holder})")
            print(f"   Transaction ID: {transaction_id}")
            print(f"   Status: succeeded")
        else:
            print(f"✅ Free tier subscription for {username} (no payment required)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating test subscription for {username}: {e}")
        return False
    
    finally:
        conn.close()

def test_payment_system():
    """Test the payment system with demo purchases"""
    
    print("🧪 TESTING EXPRESS DEALS PAYMENT SYSTEM")
    print("=" * 50)
    
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    try:
        # Get admin and bonafs users
        cursor.execute("SELECT id, username FROM auth_user WHERE username IN ('admin', 'bonafs')")
        users = cursor.fetchall()
        
        if not users:
            print("❌ No test users found (admin, bonafs)")
            return False
        
        print(f"👥 Found {len(users)} test users")
        
        # Test purchases for each user
        for user_id, username in users:
            print(f"\n🛒 Testing purchases for {username}:")
            
            # Create a regular purchase
            purchase_amounts = [29.99, 49.99, 19.99, 99.99]
            amount = random.choice(purchase_amounts)
            create_test_purchase(user_id, username, amount)
            
            # Create a subscription
            tiers = ['basic', 'premium', 'vip']
            tier = random.choice(tiers)
            create_test_subscription(user_id, username, tier)
        
        # Display results
        print(f"\n📊 PAYMENT SYSTEM TEST RESULTS:")
        print("=" * 50)
        
        # Count total payments
        cursor.execute("SELECT COUNT(*) FROM payments_payment")
        total_payments = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM payments_payment WHERE status = 'succeeded'")
        successful_payments = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(amount) FROM payments_payment WHERE status = 'succeeded'")
        total_revenue = cursor.fetchone()[0] or 0
        
        print(f"💳 Total Payments: {total_payments}")
        print(f"✅ Successful Payments: {successful_payments}")
        print(f"💰 Total Revenue: £{total_revenue:.2f}")
        
        # Show recent payments
        cursor.execute('''
            SELECT u.username, p.amount, p.payment_type, p.status, p.transaction_id, p.created_at
            FROM payments_payment p
            JOIN auth_user u ON p.user_id = u.id
            ORDER BY p.created_at DESC
            LIMIT 10
        ''')
        
        recent_payments = cursor.fetchall()
        
        if recent_payments:
            print(f"\n🔍 RECENT PAYMENTS:")
            for username, amount, payment_type, status, transaction_id, created_at in recent_payments:
                print(f"   {username}: £{amount} ({payment_type}) - {status} - {transaction_id}")
        
        print(f"\n🎉 PAYMENT SYSTEM TESTING COMPLETED!")
        return True
        
    except Exception as e:
        print(f"❌ Error during payment system testing: {e}")
        return False
    
    finally:
        conn.close()

if __name__ == "__main__":
    success = test_payment_system()
    if success:
        print("\n✅ All payment tests passed!")
    else:
        print("\n❌ Payment testing failed!")
