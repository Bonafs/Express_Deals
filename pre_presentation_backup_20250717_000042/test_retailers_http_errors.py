#!/usr/bin/env python
"""
Test script to check which supported retailers are affected by HTTP errors
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from scraping.url_tracking_service import url_tracking_service

# Test URLs for major supported retailers
test_urls = {
    'Amazon UK': 'https://www.amazon.co.uk/dp/B08N5WRWNW',
    'Currys PC World': 'https://www.currys.co.uk/products/apple-iphone-15-128-gb-blue-10253799.html',
    'John Lewis': 'https://www.johnlewis.com/apple-iphone-15-128gb/p109380951',
    'Argos': 'https://www.argos.co.uk/product/123456789',
    'ASOS': 'https://www.asos.com/nike/nike-air-max-90/prd/123456789',
    'Next': 'https://www.next.co.uk/style/st123456',
    'Tesco': 'https://www.tesco.com/groceries/en-GB/products/123456789',
    'eBay UK': 'https://www.ebay.co.uk/itm/123456789',
    'Boots': 'https://www.boots.com/product/123456789',
    'Marks & Spencer': 'https://www.marksandspencer.com/product/123456789',
    'Very': 'https://www.very.co.uk/product/123456789',
    'ASDA': 'https://groceries.asda.com/product/123456789',
    'AO.com': 'https://ao.com/product/123456789',
    'Screwfix': 'https://www.screwfix.com/p/product/123456789',
    'Sports Direct': 'https://www.sportsdirect.com/product/123456789'
}

print("Testing HTTP Error Handling for Supported Retailers")
print("=" * 60)

results = {}

for retailer_name, test_url in test_urls.items():
    print(f"\nTesting {retailer_name}...")
    print(f"URL: {test_url}")
    
    try:
        # Test URL validation
        validation_result = url_tracking_service.validate_url(test_url)
        print(f"✅ Validation: {validation_result.is_valid} - {validation_result.retailer_name}")
        
        if validation_result.is_valid:
            # Test availability check
            availability = url_tracking_service.check_product_availability(test_url, timeout=8)
            
            if availability['available']:
                print(f"✅ Status: Accessible")
                print(f"   Title: {availability.get('title', 'N/A')[:50]}...")
                print(f"   Price: {availability.get('price', 'N/A')}")
                print(f"   Response Time: {availability.get('response_time', 'N/A'):.2f}s")
            else:
                error_msg = availability.get('error', 'Unknown error')
                print(f"❌ Status: Not accessible")
                print(f"   Error: {error_msg}")
                
                # Check if it's the "HTTP error Unknown" issue
                if 'HTTP error' in error_msg and 'Unknown' in error_msg:
                    print(f"   🚨 AFFECTED BY HTTP UNKNOWN ERROR")
                    results[retailer_name] = 'HTTP_UNKNOWN_ERROR'
                elif 'HTTP error' in error_msg:
                    print(f"   ⚠️  HTTP error (but with proper status code)")
                    results[retailer_name] = 'HTTP_ERROR_WITH_CODE'
                else:
                    results[retailer_name] = 'OTHER_ERROR'
            
            # Test tracking effectiveness
            effectiveness = url_tracking_service.get_tracking_effectiveness(test_url)
            print(f"   Tracking Score: {effectiveness['score']}/100")
            
        else:
            print(f"❌ Validation failed: {validation_result.error_message}")
            results[retailer_name] = 'VALIDATION_FAILED'
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        results[retailer_name] = f'EXCEPTION: {str(e)}'
    
    print("-" * 40)

# Summary
print("\n" + "=" * 60)
print("SUMMARY OF RESULTS")
print("=" * 60)

http_unknown_errors = []
http_errors_with_codes = []
other_issues = []
working_retailers = []

for retailer, status in results.items():
    if status == 'HTTP_UNKNOWN_ERROR':
        http_unknown_errors.append(retailer)
    elif status == 'HTTP_ERROR_WITH_CODE':
        http_errors_with_codes.append(retailer)
    elif 'EXCEPTION' in status or 'ERROR' in status:
        other_issues.append(retailer)
    else:
        working_retailers.append(retailer)

print(f"\n🚨 Retailers affected by 'HTTP error Unknown': {len(http_unknown_errors)}")
for retailer in http_unknown_errors:
    print(f"   - {retailer}")

print(f"\n⚠️  Retailers with HTTP errors (but proper codes): {len(http_errors_with_codes)}")
for retailer in http_errors_with_codes:
    print(f"   - {retailer}")

print(f"\n❌ Retailers with other issues: {len(other_issues)}")
for retailer in other_issues:
    print(f"   - {retailer}")

print(f"\n✅ Working retailers: {len(working_retailers)}")
for retailer in working_retailers:
    print(f"   - {retailer}")

print(f"\nTotal retailers tested: {len(test_urls)}")
print(f"Success rate: {len(working_retailers)}/{len(test_urls)} ({len(working_retailers)/len(test_urls)*100:.1f}%)")

if http_unknown_errors:
    print(f"\n🔧 RECOMMENDATION: The 'HTTP error Unknown' fix should resolve issues for {len(http_unknown_errors)} retailers")
else:
    print(f"\n✅ No retailers affected by 'HTTP error Unknown' - the fix is working!")
