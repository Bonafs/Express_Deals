#!/usr/bin/env python
"""
Quick test for key retailers HTTP error status
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from scraping.url_tracking_service import url_tracking_service

# Test a few key retailers with likely problematic URLs
test_cases = [
    ('Amazon UK', 'https://www.amazon.co.uk/dp/INVALID123'),
    ('Currys', 'https://www.currys.co.uk/products/invalid-product-123.html'),
    ('John Lewis', 'https://www.johnlewis.com/invalid-product/p999999999'),
    ('ASOS', 'https://www.asos.com/invalid/product/prd/999999999'),
    ('Next', 'https://www.next.co.uk/invalid/st999999'),
]

print("Testing HTTP Error Handling - Key Retailers")
print("=" * 50)

for retailer, url in test_cases:
    print(f"\nTesting {retailer}: {url}")
    
    try:
        availability = url_tracking_service.check_product_availability(url, timeout=5)
        error_msg = availability.get('error', 'No error')
        
        print(f"Available: {availability['available']}")
        print(f"Error: {error_msg}")
        
        # Check for the specific "HTTP error Unknown" issue
        if 'HTTP error' in error_msg and ('Unknown' in error_msg or error_msg == 'HTTP error'):
            print("🚨 AFFECTED BY HTTP UNKNOWN ERROR!")
        elif 'HTTP error' in error_msg and any(code in error_msg for code in ['404', '403', '500', '429']):
            print("✅ HTTP error with proper status code")
        else:
            print("ℹ️  Other error type")
            
    except Exception as e:
        print(f"Exception: {e}")
    
    print("-" * 30)

print("\nTest completed!")
