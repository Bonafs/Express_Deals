#!/usr/bin/env python
"""
Test and populate price alerts for dashboard demonstration
"""
import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from django.contrib.auth.models import User
from products.models import Product
from scraping.models import PriceAlert

print("🎯 SETTING UP DASHBOARD DEMO DATA")
print("=" * 50)

# Get or create test users
admin_user = User.objects.filter(username='admin').first()
customer1 = User.objects.filter(username='customer1').first()

if not customer1:
    print("❌ Customer1 not found. Please create users first.")
    exit()

# Get some products
products = Product.objects.all()[:5]

if not products.exists():
    print("❌ No products found. Please create products first.")
    exit()

print(f"📦 Found {products.count()} products to create alerts for")

# Create sample price alerts for customer1
alerts_created = 0
for i, product in enumerate(products):
    # Create different types of alerts
    alert_data = [
        {
            'alert_type': 'below',
            'target_price': product.price * Decimal('0.8'),  # 20% discount target
            'onset_price': product.price,
            'current_price': product.price * Decimal('0.9'),  # Current 10% discount
        },
        {
            'alert_type': 'percentage',
            'percentage_threshold': 25,
            'onset_price': product.price,
            'current_price': product.price * Decimal('1.05'),  # Price increased 5%
        }
    ]
    
    for j, data in enumerate(alert_data):
        if i + j < 6:  # Limit to 6 alerts total
            alert, created = PriceAlert.objects.get_or_create(
                user=customer1,
                product=product,
                alert_type=data['alert_type'],
                defaults={
                    'target_price': data.get('target_price'),
                    'percentage_threshold': data.get('percentage_threshold'),
                    'onset_price': data['onset_price'],
                    'current_price': data['current_price'],
                    'status': 'active',
                    'email_enabled': True,
                    'push_enabled': True,
                }
            )
            if created:
                alerts_created += 1
                print(f"✅ Created {data['alert_type']} alert for {product.name}")

print(f"\n🎉 Created {alerts_created} new price alerts")
print("\n📋 DASHBOARD FEATURES READY:")
print("• Onset price tracking")
print("• Target vs current price comparison")
print("• Category filtering")
print("• Status filtering (Active, Triggered, Paused)")
print("• Price change indicators")
print("• Savings calculations")

print(f"\n🔗 Access dashboard at: http://localhost:8000/alerts/")
print("📱 Login as customer1 to see the enhanced dashboard")
