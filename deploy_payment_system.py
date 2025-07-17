#!/usr/bin/env python3
"""
Direct database setup for Express Deals Payment System
"""
import sqlite3
import os
from datetime import datetime

def setup_payment_system():
    """Set up payment system in SQLite database"""
    
    # Connect to database
    db_path = 'db.sqlite3'
    if not os.path.exists(db_path):
        print(f"❌ Database file {db_path} not found!")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("🚀 Setting up Express Deals Payment System...")
        
        # Create PaymentMethod table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments_paymentmethod (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                payment_type VARCHAR(20) NOT NULL,
                card_number VARCHAR(19) DEFAULT '',
                card_holder_name VARCHAR(100) DEFAULT '',
                expiry_month VARCHAR(2) DEFAULT '',
                expiry_year VARCHAR(4) DEFAULT '',
                cvv VARCHAR(4) DEFAULT '',
                stripe_customer_id VARCHAR(100) DEFAULT '',
                stripe_payment_method_id VARCHAR(100) DEFAULT '',
                is_demo BOOLEAN DEFAULT FALSE,
                is_default BOOLEAN DEFAULT FALSE,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES auth_user (id)
            )
        ''')
        
        # Create Payment table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments_payment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                order_id INTEGER,
                payment_method_id INTEGER,
                payment_type VARCHAR(20) DEFAULT 'one_time',
                amount DECIMAL(10, 2) NOT NULL,
                currency VARCHAR(3) DEFAULT 'GBP',
                status VARCHAR(20) DEFAULT 'pending',
                stripe_payment_intent_id VARCHAR(100) DEFAULT '',
                stripe_customer_id VARCHAR(100) DEFAULT '',
                transaction_id VARCHAR(100) UNIQUE NOT NULL,
                gateway_response TEXT DEFAULT '{}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES auth_user (id),
                FOREIGN KEY (payment_method_id) REFERENCES payments_paymentmethod (id)
            )
        ''')
        
        # Create DemoCard table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments_democard (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                card_type VARCHAR(20) NOT NULL,
                card_number VARCHAR(19) NOT NULL,
                card_holder_name VARCHAR(100) NOT NULL,
                expiry_month VARCHAR(2) NOT NULL,
                expiry_year VARCHAR(4) NOT NULL,
                cvv VARCHAR(4) NOT NULL,
                scenario VARCHAR(100) NOT NULL,
                description TEXT DEFAULT '',
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert demo cards
        demo_cards = [
            ('visa', '4242424242424242', 'John Doe', '12', '2026', '123', 'Success', 'Visa card for successful payments'),
            ('mastercard', '5555555555554444', 'Jane Smith', '11', '2025', '456', 'Success', 'Mastercard for successful payments'),
            ('amex', '378282246310005', 'Bob Johnson', '10', '2027', '789', 'Success', 'American Express for successful payments'),
            ('visa', '4000000000000002', 'Test Decline', '09', '2026', '111', 'Declined', 'Visa card that will be declined'),
            ('visa', '4000000000009995', 'Test Insufficient', '08', '2025', '222', 'Insufficient Funds', 'Visa card with insufficient funds')
        ]
        
        for card in demo_cards:
            cursor.execute('''
                INSERT OR IGNORE INTO payments_democard 
                (card_type, card_number, card_holder_name, expiry_month, expiry_year, cvv, scenario, description) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', card)
        
        # Get users and assign demo cards
        cursor.execute("SELECT id, username FROM auth_user WHERE username IN ('admin', 'bonafs')")
        users = cursor.fetchall()
        
        cursor.execute("SELECT * FROM payments_democard WHERE scenario = 'Success'")
        success_cards = cursor.fetchall()
        
        for i, (user_id, username) in enumerate(users):
            if success_cards:
                card = success_cards[i % len(success_cards)]
                masked_number = f"**** **** **** {card[2][-4:]}"  # card_number is at index 2
                
                cursor.execute('''
                    INSERT OR IGNORE INTO payments_paymentmethod 
                    (user_id, payment_type, card_number, card_holder_name, expiry_month, expiry_year, cvv, is_demo, is_default, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (user_id, 'credit_card', masked_number, card[3], card[4], card[5], card[6], 1, 1, 1))
                
                print(f"✅ Assigned demo card to {username}: {card[1]} ending in {card[2][-4:]}")
        
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_payments_user ON payments_payment(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_payments_status ON payments_payment(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_paymentmethod_user ON payments_paymentmethod(user_id)')
        
        # Commit changes
        conn.commit()
        
        # Verify setup
        cursor.execute("SELECT COUNT(*) FROM payments_democard")
        demo_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM payments_paymentmethod WHERE is_demo = 1")
        assigned_count = cursor.fetchone()[0]
        
        print(f"\n📊 SETUP COMPLETE:")
        print(f"💳 Demo Cards Created: {demo_count}")
        print(f"👥 Payment Methods Assigned: {assigned_count}")
        
        # Display assignments
        cursor.execute('''
            SELECT u.username, p.card_number, p.card_holder_name 
            FROM payments_paymentmethod p 
            JOIN auth_user u ON p.user_id = u.id 
            WHERE p.is_demo = 1
        ''')
        
        assignments = cursor.fetchall()
        if assignments:
            print("\n🎯 USER ASSIGNMENTS:")
            for username, card_number, holder_name in assignments:
                print(f"   {username}: {card_number} ({holder_name})")
        
        print("\n🚀 PAYMENT SYSTEM READY FOR TESTING!")
        return True
        
    except Exception as e:
        print(f"❌ Error setting up payment system: {e}")
        return False
    
    finally:
        conn.close()

if __name__ == "__main__":
    success = setup_payment_system()
    if success:
        print("\n✅ Payment system deployment completed successfully!")
    else:
        print("\n❌ Payment system deployment failed!")
