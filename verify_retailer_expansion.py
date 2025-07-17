#!/usr/bin/env python3
"""
Quick verification of expanded UK retailer support
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from scraping.url_tracking_service import url_tracking_service

def show_retailer_expansion():
    """Display all supported retailers with categorization"""
    
    retailers = url_tracking_service.SUPPORTED_RETAILERS
    
    print("🎯 EXPRESS DEALS - ENHANCED UK RETAILER SUPPORT")
    print("=" * 60)
    
    # Original retailers (first 6)
    original_retailers = list(retailers.keys())[:6]
    print(f"\n✅ ORIGINAL RETAILERS ({len(original_retailers)})")
    print("-" * 40)
    for i, domain in enumerate(original_retailers, 1):
        name = retailers[domain]['name']
        print(f"{i:2d}. {name:<20} ({domain})")
    
    # New retailers
    new_retailers = list(retailers.keys())[6:]
    print(f"\n🆕 NEW RETAILERS ({len(new_retailers)})")
    print("-" * 40)
    for i, domain in enumerate(new_retailers, 7):
        name = retailers[domain]['name']
        print(f"{i:2d}. {name:<20} ({domain})")
    
    print(f"\n📊 EXPANSION SUMMARY")
    print("-" * 40)
    print(f"Total Supported Retailers: {len(retailers)}")
    print(f"Market Coverage Increase: {((len(retailers) - 6) / 6 * 100):.0f}%")
    print(f"Original Count: 6")
    print(f"New Count: {len(retailers)}")
    
    # Test a few new retailers
    print(f"\n🧪 TESTING NEW RETAILER VALIDATION")
    print("-" * 40)
    
    test_retailers = [
        ('tesco.com', 'https://www.tesco.com/test'),
        ('boots.com', 'https://www.boots.com/test'),
        ('very.co.uk', 'https://www.very.co.uk/test'),
        ('ao.com', 'https://www.ao.com/test')
    ]
    
    for domain, test_url in test_retailers:
        result = url_tracking_service.validate_url(test_url)
        status = "✅" if result.is_valid else "❌"
        print(f"{status} {retailers.get(domain, {}).get('name', domain)}: {result.is_valid}")
    
    print(f"\n🚀 STATUS: Enhanced Express Deals with comprehensive UK market coverage!")

if __name__ == "__main__":
    show_retailer_expansion()
