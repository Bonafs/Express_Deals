-- Express Deals Payment System Database Setup
-- Run this directly in SQLite to create payment tables

-- PaymentMethod table
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
);

-- Payment table
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
    FOREIGN KEY (order_id) REFERENCES orders_order (id),
    FOREIGN KEY (payment_method_id) REFERENCES payments_paymentmethod (id)
);

-- RecurringPayment table
CREATE TABLE IF NOT EXISTS payments_recurringpayment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    payment_method_id INTEGER NOT NULL,
    subscription_name VARCHAR(100) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'GBP',
    frequency VARCHAR(20) NOT NULL,
    start_date TIMESTAMP NOT NULL,
    next_payment_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active',
    stripe_subscription_id VARCHAR(100) DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES auth_user (id),
    FOREIGN KEY (payment_method_id) REFERENCES payments_paymentmethod (id)
);

-- DemoCard table
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
);

-- Insert demo cards
INSERT OR IGNORE INTO payments_democard (card_type, card_number, card_holder_name, expiry_month, expiry_year, cvv, scenario, description) VALUES
('visa', '4242424242424242', 'John Doe', '12', '2026', '123', 'Success', 'Visa card for successful payments'),
('mastercard', '5555555555554444', 'Jane Smith', '11', '2025', '456', 'Success', 'Mastercard for successful payments'),
('amex', '378282246310005', 'Bob Johnson', '10', '2027', '789', 'Success', 'American Express for successful payments'),
('visa', '4000000000000002', 'Test Decline', '09', '2026', '111', 'Declined', 'Visa card that will be declined'),
('visa', '4000000000009995', 'Test Insufficient', '08', '2025', '222', 'Insufficient Funds', 'Visa card with insufficient funds');

-- Assign demo cards to users (admin and bonafs)
INSERT OR IGNORE INTO payments_paymentmethod (user_id, payment_type, card_number, card_holder_name, expiry_month, expiry_year, cvv, is_demo, is_default, is_active)
SELECT 
    u.id,
    'credit_card',
    '**** **** **** ' || substr(d.card_number, -4),
    d.card_holder_name,
    d.expiry_month,
    d.expiry_year,
    d.cvv,
    1,
    1,
    1
FROM auth_user u
CROSS JOIN payments_democard d
WHERE u.username IN ('admin', 'bonafs') AND d.scenario = 'Success'
LIMIT 2;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_payments_user ON payments_payment(user_id);
CREATE INDEX IF NOT EXISTS idx_payments_status ON payments_payment(status);
CREATE INDEX IF NOT EXISTS idx_paymentmethod_user ON payments_paymentmethod(user_id);
CREATE INDEX IF NOT EXISTS idx_recurringpayment_user ON payments_recurringpayment(user_id);

-- Test data verification
SELECT 'Demo Cards Created:' as info;
SELECT card_type, card_number, scenario FROM payments_democard;

SELECT 'Payment Methods Assigned:' as info;
SELECT u.username, p.card_number, p.card_holder_name 
FROM payments_paymentmethod p 
JOIN auth_user u ON p.user_id = u.id 
WHERE p.is_demo = 1;
